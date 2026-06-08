import json
import os
import shutil
from typing import Any, Iterable, Iterator

import requests

ORGANIZATION = "cepdnaclk"
RESULTS_PER_PAGE = 100

try:
    from dotenv import load_dotenv

except ImportError:  # pragma: no cover - optional for local execution convenience

    def load_dotenv() -> bool:
        return False


def init_env() -> None:
    """Load local environment variables when a .env file is present."""
    load_dotenv()


def load_env_var(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def safe_str(value: Any) -> str | None:
    if value is None:
        return None
    return str(value).strip()


def normalize_whitespace(value: Any) -> str:
    text = safe_str(value) or ""
    return " ".join(text.split())


def chunked(items: Iterable[Any], size: int) -> Iterator[list[Any]]:
    bucket: list[Any] = []
    for item in items:
        bucket.append(item)
        if len(bucket) >= size:
            yield bucket
            bucket = []
    if bucket:
        yield bucket


def log_event(stage: str, message: str, level: str = "INFO", **context: Any) -> None:
    payload = {"level": level, "stage": stage, "message": message}
    if context:
        payload["context"] = context
    print(json.dumps(payload, ensure_ascii=False))


def get_custom_media(default_cover, default_thumb, gh_page):
    """
    Fast existence check for custom cover and thumbnail using HEAD (falls back to GET if needed).
    """
    cover_url = default_cover
    thumbnail_url = default_thumb

    if gh_page == "blank":
        return cover_url, thumbnail_url

    session = requests.Session()
    session.headers.update({"User-Agent": "RepoIndexer/MediaCheck"})

    # Quick reachability test for the GH Pages site
    try:
        root_resp = session.head(gh_page, timeout=3, allow_redirects=True)
        if root_resp.status_code >= 400:
            return cover_url, thumbnail_url
    except requests.RequestException:
        return cover_url, thumbnail_url

    def exists(url):
        try:
            resp = session.head(url, timeout=3, allow_redirects=True)
            if resp.status_code == 200:
                return True
            if resp.status_code in (403, 405):  # HEAD not allowed; try lightweight GET
                get_resp = session.get(url, timeout=5, stream=True)
                get_resp.close()
                return get_resp.status_code == 200
        except requests.RequestException:
            return False
        return False

    cover_candidate = f"{gh_page}/data/cover_page.jpg"
    if exists(cover_candidate):
        cover_url = cover_candidate

    thumb_candidate = f"{gh_page}/data/thumbnail.jpg"
    if exists(thumb_candidate):
        thumbnail_url = thumb_candidate

    return cover_url, thumbnail_url


def load_category_data(url="../data/categories/index.json"):
    """
    Loads category data from the specified index file and initializes batch sets.
    Returns a tuple of (categories, batches) where:
    - categories: A dictionary mapping category keys to their data.
    - batches: A dictionary mapping category links to sets of batch names.
    """

    categories = {}
    batches = {}

    # Load category index data
    with open(url, "r", encoding="utf-8") as f:
        category_data = json.load(f)

    # Load each category's data and initialize batch sets
    for i in category_data:
        with open(f"../data/categories/{i}/index.json", "r", encoding="utf-8") as f:
            categories[i] = json.load(f)

        batches[category_data[i]["link"]] = set()

    return categories, batches


def delete_category_index(dir_path="../categories/"):
    """
    Deletes the specified directory and all its contents.
    """
    try:
        shutil.rmtree(dir_path)
    except OSError as e:
        print("Error: %s : %s" % (dir_path, e.strerror))


def delete_project_index(dir_path="../projects/github_projects/"):
    """
    Deletes the specified directory and all its contents.
    """
    try:
        shutil.rmtree(dir_path)
    except OSError as e:
        print("Error: %s : %s" % (dir_path, e.strerror))


def download_repository_data(
    organization=ORGANIZATION, results_per_page=RESULTS_PER_PAGE
):
    """
    Downloads repository data for the specified organization using the GitHub API.
    Returns a dictionary mapping repository names to their data.

    Raises:
        requests.RequestException: If the API request fails or returns an error status.
    """
    repo_dict = {}
    for p in range(1, 1000):
        url = (
            f"https://api.github.com/orgs/{organization}/repos?"
            f"per_page={results_per_page}&page={p}"
        )
        response = requests.get(url)

        if response.status_code == 200:
            jsonData = response.json()
            if len(jsonData) == 0:
                break

            for repo in jsonData:
                repo_dict[repo["name"]] = repo

        else:
            raise requests.RequestException(
                f"Failed to fetch data: {response.status_code} - {response.text}"
            )

    return repo_dict
