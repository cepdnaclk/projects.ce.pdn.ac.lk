import hashlib
import json
from typing import Any
from urllib.parse import urlparse

from .helpers import normalize_whitespace, safe_str

PLACEHOLDER_VALUES = {"", "#", "n/a", "na", "none", "null", "nil", "-"}
MAX_DESCRIPTION_LENGTH = 480


def is_placeholder(value: Any) -> bool:
    text = (safe_str(value) or "").strip().lower()
    return text in PLACEHOLDER_VALUES


def sanitize_url(value: Any) -> str | None:
    text = safe_str(value)
    if not text or is_placeholder(text):
        return None

    parsed = urlparse(text)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return None

    return text


def sanitize_email(value: Any) -> str | None:
    text = normalize_whitespace(value)
    if not text or is_placeholder(text) or "@" not in text:
        return None
    return text


def normalize_tags(tags: Any) -> list[str]:
    if not isinstance(tags, list):
        return []

    result: list[str] = []
    seen: set[str] = set()
    for tag in tags:
        text = normalize_whitespace(tag)
        if not text or is_placeholder(text):
            continue
        folded = text.casefold()
        if folded in seen:
            continue
        seen.add(folded)
        result.append(text)
    return result


def trim_description(value: Any, max_length: int = MAX_DESCRIPTION_LENGTH) -> str:
    text = normalize_whitespace(value)
    if len(text) <= max_length:
        return text

    clipped = text[: max_length - 3].rstrip()
    return f"{clipped}..."


def sanitize_people_map(value: Any) -> dict[str, dict[str, str | None]]:
    if not isinstance(value, dict):
        return {}

    people: dict[str, dict[str, str | None]] = {}
    for raw_key, raw_person in value.items():
        key = normalize_whitespace(raw_key)
        if not key or not isinstance(raw_person, dict):
            continue

        person = {
            "name": normalize_whitespace(raw_person.get("name")) or None,
            "email": sanitize_email(raw_person.get("email")),
            "profile_url": sanitize_url(raw_person.get("profile_url")),
            "profile_image": sanitize_url(raw_person.get("profile_image")),
        }

        if any(person.values()):
            people[key] = person

    return people


def flatten_person_field(
    people: dict[str, dict[str, str | None]], field: str
) -> list[str]:
    values: list[str] = []
    seen: set[str] = set()
    for person in people.values():
        value = person.get(field)
        if not value:
            continue
        folded = value.casefold()
        if folded in seen:
            continue
        seen.add(folded)
        values.append(value)
    return values


def select_result_url(record: dict[str, Any]) -> str:
    for field in ("project_url", "page_url", "repo_url", "api_url"):
        if record.get(field):
            return record[field]
    return "#"


def build_project_record(object_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    object_id = normalize_whitespace(object_id)
    if not object_id:
        raise ValueError("Record is missing a stable objectID")

    title = normalize_whitespace(payload.get("title"))
    if not title:
        raise ValueError(f"Record {object_id} is missing a title")

    category = (
        payload.get("category") if isinstance(payload.get("category"), dict) else {}
    )
    team = sanitize_people_map(payload.get("team"))
    supervisors = sanitize_people_map(payload.get("supervisors"))

    record = {
        "objectID": object_id,
        "title": title,
        "description": trim_description(payload.get("description")),
        "category_title": normalize_whitespace(category.get("title")),
        "category_code": normalize_whitespace(category.get("code")),
        "project_url": sanitize_url(payload.get("project_url")),
        "repo_url": sanitize_url(payload.get("repo_url")),
        "page_url": sanitize_url(payload.get("page_url")),
        "api_url": sanitize_url(payload.get("api_url")),
        "thumbnail_url": sanitize_url(payload.get("thumbnail_url")),
        "tags": normalize_tags(payload.get("tags")),
        "team": team,
        "supervisors": supervisors,
        "team_names": flatten_person_field(team, "name"),
        "team_emails": flatten_person_field(team, "email"),
        "supervisor_names": flatten_person_field(supervisors, "name"),
        "supervisor_emails": flatten_person_field(supervisors, "email"),
    }
    record["result_url"] = select_result_url(record)
    return record


def transform_projects_payload(
    payload: Any,
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    if not isinstance(payload, dict):
        raise TypeError(
            "Projects API response must be a JSON object keyed by project identifier"
        )

    records: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []

    for object_id, raw_project in payload.items():
        if not isinstance(raw_project, dict):
            errors.append(
                {
                    "objectID": normalize_whitespace(object_id),
                    "reason": "Project payload is not a JSON object",
                }
            )
            continue

        try:
            records.append(build_project_record(object_id, raw_project))
        except ValueError as exc:
            errors.append(
                {"objectID": normalize_whitespace(object_id), "reason": str(exc)}
            )

    return records, errors


def canonicalize_record(record: dict[str, Any]) -> str:
    return json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def checksum_record(record: dict[str, Any]) -> str:
    return hashlib.sha1(canonicalize_record(record).encode("utf-8")).hexdigest()


def diff_records(
    existing_records: list[dict[str, Any]], target_records: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], list[str]]:
    existing_by_id = {
        record["objectID"]: record
        for record in existing_records
        if record.get("objectID")
    }
    target_by_id = {
        record["objectID"]: record
        for record in target_records
        if record.get("objectID")
    }

    to_upsert: list[dict[str, Any]] = []
    for object_id, target in target_by_id.items():
        existing = existing_by_id.get(object_id)
        if existing is None or checksum_record(existing) != checksum_record(target):
            to_upsert.append(target)

    to_delete = sorted(set(existing_by_id) - set(target_by_id))
    return to_upsert, to_delete
