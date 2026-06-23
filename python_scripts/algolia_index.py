"""Sync project records from api.ce.pdn.ac.lk into Algolia."""

from __future__ import annotations

import sys

import requests
from algoliasearch.search_client import SearchClient
from util.configs import PROJECTS_IDX_SETTINGS
from util.helpers import load_env_var, transform_projects_payload

PROJECTS_API_URL = "https://api.ce.pdn.ac.lk/projects/v1/all/"
ALGOLIA_PROJECTS_INDEX_NAME = "project_index"
REQUEST_TIMEOUT = 60
MAX_DESCRIPTION_LENGTH = 1000


class IndexingError(RuntimeError):
    """Raised when the indexing pipeline encounters a fatal error."""


def fetch_projects_list(url: str) -> dict:
    """
    Fetches the list of projects from the specified API URL and returns it as a dictionary.
    Raises an IndexingError if the request fails, returns a non-200 status code,
    """

    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
    except requests.RequestException as exc:
        raise IndexingError(f"Request failed for {url}: {exc}") from exc

    if response.status_code >= 400:
        body = response.text[:1000]
        raise IndexingError(
            f"Request failed for {url} with status {response.status_code}: {body}"
        )

    try:
        payload = response.json()
    except ValueError as exc:
        raise IndexingError(f"Invalid JSON returned from {url}") from exc

    if not isinstance(payload, dict):
        raise IndexingError("Projects API did not return a JSON object")
    return payload


def prepare_records(records: list[dict]) -> list[dict]:
    prepared = []
    for record in records:
        prepared_record = record.copy()
        description = prepared_record.get("description")
        if description:
            prepared_record["description"] = description.strip()[
                :MAX_DESCRIPTION_LENGTH
            ]
        prepared.append(prepared_record)
    return prepared


def wait_for_task(index, response):
    if isinstance(response, dict) and "taskID" in response:
        index.wait_task(response["taskID"])


def sync(index, records: list[dict], settings: dict) -> None:
    if not isinstance(settings, dict):
        raise TypeError("Algolia index settings must be a dictionary")

    prepared_records = prepare_records(records)
    print(f"Uploading {len(prepared_records)} records to '{index.name}'")

    wait_for_task(index, index.replace_all_objects(prepared_records))
    wait_for_task(index, index.set_settings(settings))


def main() -> int:
    try:
        client = SearchClient.create(
            app_id=load_env_var("ALGOLIA_APP_ID"),
            api_key=load_env_var("ALGOLIA_ADMIN_API_KEY"),
        )

        payload = fetch_projects_list(PROJECTS_API_URL)
        project_records, record_errors = transform_projects_payload(payload)
        print(
            f"Transformed project payload; count={len(project_records)}, skipped={len(record_errors)}"
        )

        if record_errors:
            print(
                f"Skipped {len(record_errors)} malformed record(s) during transformation"
            )

        sync(
            client.init_index(ALGOLIA_PROJECTS_INDEX_NAME),
            records=project_records,
            settings=PROJECTS_IDX_SETTINGS,
        )
        print("Algolia indexing completed successfully!")
        return 0
    except Exception:
        print("Algolia indexing failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
