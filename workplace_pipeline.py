"""Shared helpers for the synthetic workplace retrieval lab."""

import json
import re
from pathlib import Path


STOP_WORDS = {
    "a", "an", "the", "is", "are", "do", "does", "how",
    "what", "which", "of", "to", "for", "per", "in",
    "on", "and", "or", "with",
}


class ConfigurationError(ValueError):
    pass


class AccessDeniedError(PermissionError):
    pass


class SourceDataError(RuntimeError):
    pass


class RequestValidationError(ValueError):
    pass


def tokenize(text):
    return set(re.findall(r"[a-z0-9]+", text.lower())) - STOP_WORDS


def validate_top_k(top_k):
    if type(top_k) is not int or not 1 <= top_k <= 10:
        raise ConfigurationError(
            "top_k must be an integer from 1 through 10."
        )


def validate_question(question):
    if not isinstance(question, str) or not question.strip():
        raise RequestValidationError("A non-empty query is required.")

    tokens = tokenize(question)

    if not tokens:
        raise RequestValidationError("Query has no searchable tokens.")

    return tokens


def resolve_project_path(project_root, relative_path):
    if not isinstance(relative_path, str) or not relative_path:
        raise ConfigurationError("A project-relative path is required.")

    path = Path(relative_path)

    if path.is_absolute() or path.drive or path.root:
        raise ConfigurationError("Absolute paths are not permitted.")

    root = Path(project_root).resolve()
    resolved = (root / path).resolve()

    if not resolved.is_relative_to(root):
        raise ConfigurationError("Path escapes the project root.")

    return resolved


def read_json_object(path):
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ConfigurationError(
            "Configuration file could not be read as JSON."
        ) from error

    if not isinstance(value, dict):
        raise ConfigurationError("Configuration must be a JSON object.")

    return value


def load_authorized_passages(project_root, policy_relative_path, role):
    policy_path = resolve_project_path(project_root, policy_relative_path)
    policy = read_json_object(policy_path)

    roles = policy.get("roles")
    documents = policy.get("documents")

    if (
        not isinstance(roles, list)
        or not roles
        or any(not isinstance(item, str) or not item for item in roles)
        or len(set(roles)) != len(roles)
        or not isinstance(documents, list)
        or not documents
    ):
        raise ConfigurationError("Invalid role or document definitions.")

    if not isinstance(role, str) or role not in roles:
        raise AccessDeniedError("Unrecognized role.")

    validated_documents = []
    seen_ids = set()
    seen_paths = set()

    # Validate every entry before reading document contents.
    for document in documents:
        if not isinstance(document, dict):
            raise ConfigurationError("Invalid document entry.")

        document_id = document.get("id")
        allowed_roles = document.get("allowed_roles")

        if (
            not isinstance(document_id, str)
            or not document_id
            or not isinstance(allowed_roles, list)
            or not allowed_roles
            or any(
                not isinstance(item, str) or item not in roles
                for item in allowed_roles
            )
        ):
            raise ConfigurationError("Invalid document permissions.")

        path = resolve_project_path(project_root, document.get("path"))

        if document_id in seen_ids or path in seen_paths:
            raise ConfigurationError("Duplicate document ID or path.")

        seen_ids.add(document_id)
        seen_paths.add(path)
        validated_documents.append((document_id, path, allowed_roles))

    passages = []
    read_ids = []

    for document_id, path, allowed_roles in validated_documents:
        if role not in allowed_roles:
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            raise SourceDataError(
                "An authorized document could not be read."
            ) from error

        read_ids.append(document_id)
        _, separator, body = text.partition("\n\n")

        if not separator or not body.strip():
            raise SourceDataError("An authorized document has no policy body.")

        for line_number, line in enumerate(body.splitlines(), start=1):
            sentence = line.strip()

            if sentence:
                passages.append({
                    "document_id": document_id,
                    "passage_id": f"{document_id}:{line_number}",
                    "text": sentence,
                    "tokens": tokenize(sentence),
                })

    return passages, read_ids

from datetime import datetime, timezone
from time import perf_counter
from uuid import uuid4


def retrieve_request(project_root, config_relative_path, question, role, log_path):
    request_id = uuid4().hex
    started = perf_counter()
    results = []
    status = "error"
    error_code = None
    config_version = None

    try:
        config_path = resolve_project_path(project_root, config_relative_path)
        configuration = read_json_object(config_path)

        if configuration.get("schema_version") != "1.0":
            raise ConfigurationError("Unsupported configuration schema.")

        version = configuration.get("version")
        if not isinstance(version, str) or not version:
            raise ConfigurationError("A configuration version is required.")

        config_version = version
        top_k = configuration.get("top_k")
        validate_top_k(top_k)
        query_tokens = validate_question(question)

        passages, _ = load_authorized_passages(
            project_root,
            configuration.get("policy_path"),
            role,
        )

        for passage in passages:
            score = len(query_tokens & passage["tokens"])

            if score:
                results.append({
                    "document_id": passage["document_id"],
                    "passage_id": passage["passage_id"],
                    "text": passage["text"],
                    "score": score,
                })

        results.sort(key=lambda item: (-item["score"], item["passage_id"]))
        results = results[:top_k]
        status = "ok" if results else "no_match"

    except ConfigurationError:
        error_code = "INVALID_CONFIGURATION"
    except RequestValidationError:
        error_code = "INVALID_QUERY"
    except AccessDeniedError:
        error_code = "ACCESS_DENIED"
    except SourceDataError:
        error_code = "SOURCE_UNAVAILABLE_OR_INVALID"

    event = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "request_id": request_id,
        "event": "retrieval_completed",
        "config_version": config_version,
        "status": status,
        "error_code": error_code,
        "result_count": len(results),
        "elapsed_ms": round((perf_counter() - started) * 1000, 3),
    }

    # The log path is supplied by the notebook operator, not the query.
    # Log-write failures propagate.
    with Path(log_path).open("a", encoding="utf-8") as file:
        file.write(json.dumps(event) + "\n")

    return {**event, "results": results}