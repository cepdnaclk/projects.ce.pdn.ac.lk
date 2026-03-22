"""Sync project records from api.ce.pdn.ac.lk into Algolia."""

from __future__ import annotations

import sys
import time
from typing import Any

import requests
from util.algolia_projects import diff_records, transform_projects_payload
from util.configs import PROJECTS_IDX_SETTINGS
from util.helpers import chunked, init_env, load_env_var, log_event

PROJECTS_API_URL = "https://api.ce.pdn.ac.lk/projects/v1/all/"
ALGOLIA_PROJECTS_INDEX_NAME = "project_index"
ALGOLIA_BATCH_SIZE = 250
REQUEST_TIMEOUT = 60


class IndexingError(RuntimeError):
    """Raised when the indexing pipeline encounters a fatal error."""


def request_json(
    method: str,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    json_body: dict[str, Any] | None = None,
    params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    try:
        response = requests.request(
            method,
            url,
            headers=headers,
            json=json_body,
            params=params,
            timeout=REQUEST_TIMEOUT,
        )
    except requests.RequestException as exc:
        raise IndexingError(f"Request failed for {url}: {exc}") from exc

    if response.status_code >= 400:
        body = response.text[:1000]
        raise IndexingError(
            f"Request failed for {url} with status {response.status_code}: {body}"
        )

    try:
        return response.json()
    except ValueError as exc:
        raise IndexingError(f"Invalid JSON returned from {url}") from exc


def algolia_headers(app_id: str, api_key: str) -> dict[str, str]:
    return {
        "X-Algolia-Application-Id": app_id,
        "X-Algolia-API-Key": api_key,
        "Content-Type": "application/json",
    }


def algolia_base_url(app_id: str) -> str:
    return f"https://{app_id}.algolia.net/1/indexes"


def fetch_projects_payload(api_url: str) -> dict[str, Any]:
    log_event("fetch", "Fetching project records", url=api_url)
    payload = request_json("GET", api_url)
    if not isinstance(payload, dict):
        raise IndexingError("Projects API did not return a JSON object")
    log_event("fetch", "Fetched project records", record_count=len(payload))
    return payload


def browse_index(app_id: str, admin_key: str, index_name: str) -> list[dict[str, Any]]:
    headers = algolia_headers(app_id, admin_key)
    url = f"{algolia_base_url(app_id)}/{index_name}/browse"

    all_hits: list[dict[str, Any]] = []
    cursor: str | None = None

    while True:
        body = {"cursor": cursor} if cursor else {"params": "hitsPerPage=1000"}
        try:
            page = request_json("POST", url, headers=headers, json_body=body)
        except IndexingError as exc:
            if "status 404" in str(exc):
                log_event(
                    "diff",
                    "Algolia index does not exist yet. Treating existing dataset as empty.",
                    level="WARNING",
                    index_name=index_name,
                )
                return []
            raise
        hits = page.get("hits")
        if not isinstance(hits, list):
            raise IndexingError("Algolia browse response did not include a hits array")
        all_hits.extend(hits)
        cursor = page.get("cursor")
        if not cursor:
            break

    log_event("diff", "Fetched existing Algolia records", record_count=len(all_hits))
    return all_hits


def wait_for_task(
    app_id: str, admin_key: str, index_name: str, task_id: int | None
) -> None:
    if task_id is None:
        return

    headers = algolia_headers(app_id, admin_key)
    url = f"{algolia_base_url(app_id)}/{index_name}/task/{task_id}"
    for _ in range(60):
        response = request_json("GET", url, headers=headers)
        if response.get("status") == "published":
            return
        time.sleep(1)
    raise IndexingError(f"Timed out waiting for Algolia task {task_id}")


def apply_settings(app_id: str, admin_key: str, index_name: str) -> None:
    headers = algolia_headers(app_id, admin_key)
    url = f"{algolia_base_url(app_id)}/{index_name}/settings"
    log_event("settings", "Applying Algolia index settings", index_name=index_name)
    response = request_json(
        "PUT", url, headers=headers, json_body=PROJECTS_IDX_SETTINGS
    )
    wait_for_task(app_id, admin_key, index_name, response.get("taskID"))


def upsert_records(
    app_id: str, admin_key: str, index_name: str, records: list[dict[str, Any]]
) -> None:
    if not records:
        log_event("upsert", "No records to upsert")
        return

    headers = algolia_headers(app_id, admin_key)
    base_url = algolia_base_url(app_id)
    last_task_id: int | None = None

    for batch in chunked(records, ALGOLIA_BATCH_SIZE):
        for record in batch:
            object_id = record["objectID"]
            url = f"{base_url}/{index_name}/{object_id}"
            response = request_json("PUT", url, headers=headers, json_body=record)
            last_task_id = response.get("taskID", last_task_id)

    wait_for_task(app_id, admin_key, index_name, last_task_id)
    log_event("upsert", "Upserted Algolia records", record_count=len(records))


def delete_records(
    app_id: str, admin_key: str, index_name: str, object_ids: list[str]
) -> None:
    if not object_ids:
        log_event("delete", "No stale records to delete")
        return

    headers = algolia_headers(app_id, admin_key)
    base_url = algolia_base_url(app_id)
    last_task_id: int | None = None

    for batch in chunked(object_ids, ALGOLIA_BATCH_SIZE):
        for object_id in batch:
            url = f"{base_url}/{index_name}/{object_id}"
            response = request_json("DELETE", url, headers=headers)
            last_task_id = response.get("taskID", last_task_id)

    wait_for_task(app_id, admin_key, index_name, last_task_id)
    log_event("delete", "Deleted stale Algolia records", record_count=len(object_ids))


def main() -> int:
    try:
        init_env()
        app_id = load_env_var("ALGOLIA_APP_ID")
        admin_key = load_env_var("ALGOLIA_ADMIN_API_KEY")
        index_name = ALGOLIA_PROJECTS_INDEX_NAME

        payload = fetch_projects_payload(PROJECTS_API_URL)
        records, record_errors = transform_projects_payload(payload)
        log_event(
            "transform",
            "Transformed project payload",
            record_count=len(records),
            skipped_count=len(record_errors),
        )
        if record_errors:
            log_event(
                "transform",
                "Skipped malformed records during transformation",
                level="WARNING",
                skipped=record_errors[:10],
            )

        existing_records = browse_index(app_id, admin_key, index_name)
        upsert_records_list, delete_records_list = diff_records(
            existing_records, records
        )
        log_event(
            "diff",
            "Computed Algolia delta",
            fetched_count=len(records),
            existing_count=len(existing_records),
            upsert_count=len(upsert_records_list),
            delete_count=len(delete_records_list),
        )

        apply_settings(app_id, admin_key, index_name)
        upsert_records(app_id, admin_key, index_name, upsert_records_list)
        delete_records(app_id, admin_key, index_name, delete_records_list)
        log_event(
            "complete", "Algolia indexing completed successfully", index_name=index_name
        )
        return 0
    except Exception as exc:
        log_event("failure", "Algolia indexing failed", level="ERROR", error=str(exc))
        return 1


if __name__ == "__main__":
    sys.exit(main())
