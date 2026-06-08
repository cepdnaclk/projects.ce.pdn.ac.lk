"""Sync project records from api.ce.pdn.ac.lk into Algolia."""

from __future__ import annotations

import sys
from typing import Any

import requests
from algoliasearch.search_client import SearchClient
from util.configs import PROJECTS_IDX_SETTINGS
from util.helpers import init_env, load_env_var, log_event, transform_projects_payload

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


def sync(index, records, settings):
    MAX_CONTENT = 1000
    if not isinstance(settings, dict):
        raise TypeError("Algolia index settings must be a dictionary")

    # Truncate large content fields
    updated_records = []

    for rec in records:
        # No longer chunking content - just truncate to max length

        # content = rec.get("content")
        # if isinstance(content, str) and len(content) > MAX_CONTENT:
        #     # Split oversized content into multiple chunked records
        #     start = 0
        #     chunk_idx = 1
        #     while start < len(content):
        #         chunk_content = content[start : start + MAX_CONTENT]
        #         new_rec = rec.copy()
        #         new_rec["content"] = chunk_content
        #         new_rec["chunk"] = chunk_idx
        #         if "objectID" in rec:
        #             new_rec["objectID"] = f"{rec['objectID']}#c{chunk_idx}"
        #         updated_records.append(new_rec)
        #         start += MAX_CONTENT
        #         chunk_idx += 1
        #     continue

        if rec.get("description"):
            rec["description"] = rec.get("description").strip()[:MAX_CONTENT]

        updated_records.append(rec)

    print(
        f"Uploading {len(records)} records to '{index.name}' via {len(updated_records)} chunks"
    )

    r = index.replace_all_objects(updated_records)
    if isinstance(r, dict) and "taskID" in r:
        index.wait_task(r["taskID"])
    r = index.set_settings(settings)
    if isinstance(r, dict) and "taskID" in r:
        index.wait_task(r["taskID"])
    print(f"Completed '{index.name}'")


def main() -> int:
    # try:
    if True:
        init_env()

        client = SearchClient.create(
            app_id=load_env_var("ALGOLIA_APP_ID"),
            api_key=load_env_var("ALGOLIA_ADMIN_API_KEY"),
        )

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

        project_records = records.copy()
        sync(
            client.init_index(ALGOLIA_PROJECTS_INDEX_NAME),
            project_records,
            PROJECTS_IDX_SETTINGS,
        )
        # existing_records = browse_index(app_id, admin_key, index_name)
        # upsert_records_list, delete_records_list = diff_records(
        #     existing_records, records
        # )
        # log_event(
        #     "diff",
        #     "Computed Algolia delta",
        #     fetched_count=len(records),
        #     existing_count=len(existing_records),
        #     upsert_count=len(upsert_records_list),
        #     delete_count=len(delete_records_list),
        # )

        # apply_settings(app_id, admin_key, index_name)
        # upsert_records(app_id, admin_key, index_name, upsert_records_list)
        # delete_records(app_id, admin_key, index_name, delete_records_list)
        # log_event(
        #     "complete", "Algolia indexing completed successfully", index_name=index_name
        # )
        return 0
    # except Exception as exc:
    #     log_event("failure", "Algolia indexing failed", level="ERROR", error=str(exc))
    #     return 1


if __name__ == "__main__":
    sys.exit(main())
