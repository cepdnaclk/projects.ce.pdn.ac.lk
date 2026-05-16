"""
REQUIREMENTS:
    pip install requests pyyaml

AUTHORS:
    Gihan Jayatilake
    Nuwan Jaliyagoda
    Akila Karunanayake
"""

import json
import os

import requests
import yaml
from notifications import Notifications
from util.helpers import (
    delete_category_index,
    delete_project_index,
    get_custom_media,
    load_category_data,
)

notify = Notifications("projects.ce.pdn.ac.lk", "Daily_Site_Builder")


excludedReposList = [
    "e03-final-year-projects",
    "e04-final-year-projects",
    "e05-final-year-projects",
]

print("START")

projects = []

# -----------------------------------------------------------------------------------
# Load Category data
CATEGORIES, BATCHES = load_category_data()

# -----------------------------------------------------------------------------------
# Delete category/project index files
delete_category_index()
delete_project_index()

# -----------------------------------------------------------------------------------
# # Download the repository data
# try:
#     repo_dict = download_repository_data()
# except requests.RequestException:
#     ERROR_MSG = "An exception occurred while getting data from GitHub: "
#     print(">> Error:", ERROR_MSG)
#     notify.warning(ERROR_MSG)

# # -----------------------------------------------------------------------------------
# # Write the repository data to a local source
# cache_file_path = "./__cache/repos.json"
# os.makedirs(os.path.dirname(cache_file_path), exist_ok=True)
# with open(cache_file_path, "w") as f:
#     json.dump(repo_dict, f, indent=4)

# -----------------------------------------------------------------------------------
# Read the repository data from a local source
with open("./__cache/repos.json", "r") as f:
    repo_dict = json.load(f)


# -----------------------------------------------------------------------------------
# Iterate through the repositories in the GitHub
count = 0
for k, r in repo_dict.items():
    try:
        r_name = r["name"].strip().split("-")

        # Exclude the repository by definition
        IS_EXCLUDED_REPO = r["name"] in excludedReposList

        # Exclude duplicated / self-forked repositories
        if str(r_name[-1]).isdigit() and "-".join(r_name[:-1]) in repo_dict:
            print(f">> Error: Duplicate repository | {r['name']}")
            IS_EXCLUDED_REPO = True

        # General eligibility check to be a Student Project
        if all(
            (
                r_name[0][0] == "e",
                r_name[0][1:].isdigit(),
                len(r_name) > 2,
                not IS_EXCLUDED_REPO,
            )
        ):
            batch = f"e{int(r_name[0][1:]):02d}"
            cat = r_name[1].lower()

            TITLE = " ".join(r_name[2:])
            FILENAME = "-".join(r_name[2:])

            count += 1
            print(f">> {cat} > {batch} > {TITLE}")

            # Check about whether the project belong to any allowed project category
            if cat not in CATEGORIES:
                print(f">> Error: Not belonged to a category | {r['name']}")
                continue

            cat_name = CATEGORIES[cat]["title"]
            cat_cover = CATEGORIES[cat]["images"]["cover"]
            cat_thumb = CATEGORIES[cat]["images"]["thumbnail"]

            GH_PAGE = (
                f"https://cepdnaclk.github.io/{r['name']}" if r["has_pages"] else None
            )
            desc = (
                r["description"].strip().replace('"', "'") if r["description"] else ""
            )
            cover_url, thumbnail_url = get_custom_media(
                default_cover=f"/data/categories/{cat}/{cat_cover}",
                default_thumb=f"/data/categories/{cat}/{cat_thumb}",
                gh_page=GH_PAGE,
            )

            data = {
                "layout": "project_page",
                "title": TITLE,
                "permalink": f"/{cat}/{batch}/{FILENAME}/",
                "description": str(desc),
                "has_children": False,
                "parent": f"{batch.upper()} {cat_name}",
                "grand_parent": cat_name,
                "cover_url": cover_url,
                "thumbnail_url": thumbnail_url,
                "repo_url": r["html_url"],
                "page_url": GH_PAGE,
                "forks": r["forks_count"],
                "watchers": r["watchers_count"],
                "stars": r["stargazers_count"],
                "started_on": r["created_at"],
            }
            description = desc.replace('"', "'")

            # Write the project file
            PATH = f"../projects/github_projects/{cat}/{batch}/{FILENAME}.md"
            os.makedirs(os.path.dirname(PATH), exist_ok=True)
            with open(PATH, "w+", encoding="utf-8") as f:
                f.write("---\n")
                f.write(yaml.dump(data, sort_keys=False))
                f.write("---\n\n")
                f.write(description)

            BATCHES[cat].add(batch)

    except (KeyError, ValueError, OSError, requests.RequestException) as e:
        ERROR_MSG = (
            f"Repository processing failed for {r.get('name', '<unknown>')}: "
            f"{type(e).__name__}: {e}"
        )
        print(">> Error:", ERROR_MSG, e)
        notify.warning(ERROR_MSG, str(e))

print(f">> Evaluated {count} project repositories")

# -----------------------------------------------------------------------------------
# Generate the index files

for id, cat in enumerate(sorted(BATCHES)):
    cat_data = CATEGORIES[cat]
    read_more_link = cat_data["read_more"] if ("read_more" in cat_data) else "#"

    index_file = {
        "layout": "project_cat",
        "title": cat_data["title"],
        "nav_order": str(id),
        "permalink": f"/{cat}/",
        "has_children": True,
        "code": cat,
        "type": cat_data["type"],
        "parent": "Home",
        "has_toc": True,
        "search_exclude": True,
        "read_more": read_more_link,
        "default_thumb_image": f"/data/categories/{cat}/{cat_data['images']['thumbnail']}",
        "description": cat_data["description"],
    }

    # Write the category index file
    try:
        print(">> Write category index for", cat)
        PATH = "../categories/" + str(cat) + "/index.md"
        os.makedirs(os.path.dirname(PATH), exist_ok=True)
        with open(PATH, "w") as f:
            f.write("---\n")
            f.write(yaml.dump(index_file, sort_keys=False))
            f.write("---\n")

    except Exception as e:
        ERROR_MSG = f"An exception occurred while writing index file for {cat}"
        print(">> Error:", ERROR_MSG, str(e))
        notify.warning(ERROR_MSG, str(e))

    # Write batch index files for each batch under the category
    for batch in BATCHES[cat]:
        batch_file = {
            "layout": "project_batch",
            "title": f"E{batch[1:]} {cat_data['title']}",
            "permalink": f"/{cat}/{batch}/",
            "has_children": True,
            "parent": cat_data["title"],
            "batch": batch,
            "code": str(cat),
            "read_more": read_more_link,
            "search_exclude": True,
            "default_thumb_image": f"/data/categories/{cat}/{cat_data['images']['thumbnail']}",
            "description": cat_data["description"],
        }

        try:
            PATH = f"../categories/{cat_data['code']}/{batch}.md"
            os.makedirs(os.path.dirname(PATH), exist_ok=True)
            with open(PATH, "w") as f2:
                f2.write("---\n")
                f2.write(yaml.dump(batch_file, sort_keys=False))
                f2.write("---\n")

        except Exception as e:
            ERROR_MSG = (
                f"An exception occurred while writing index file for {cat}/{batch}"
            )
            print(">> Error:", ERROR_MSG, str(e))
            notify.warning(ERROR_MSG, str(e))

print(f">> Created {id} categories")

print("END")
