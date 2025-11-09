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
import shutil

import requests
import yaml
from notifications import Notifications

notify = Notifications("projects.ce.pdn.ac.lk", "Daily_Site_Builder")

CATEGORIES = {}
BATCHES = {}
ORGANIZATION = "cepdnaclk"
RESULTS_PER_PAGE = 100
excludedReposList = [
    "e03-final-year-projects",
    "e04-final-year-projects",
    "e05-final-year-projects",
]
projects = []

print("START")


def get_custom_media(default_cover, default_thumb, gh_page):
    cover_url = default_cover
    thumbnail_url = default_thumb

    if gh_page != "blank":
        # Cover
        try_cover_url = f"{gh_page}/data/cover_page.jpg"
        print("Trying cover URL:", try_cover_url)

        response_cover = requests.get(try_cover_url)
        if response_cover.status_code == 200:
            cover_url = try_cover_url

        # Thumbnail
        try_thumbnail_url = f"{gh_page}/data/thumbnail.jpg"
        print("Trying thumbnail URL:", try_thumbnail_url)

        response_thumbnail = requests.get(try_thumbnail_url)
        if response_thumbnail.status_code == 200:
            thumbnail_url = try_thumbnail_url

    return cover_url, thumbnail_url


# -----------------------------------------------------------------------------------
# Load Category data
url = "../data/categories/index.json"
with open(url, "r") as f:
    category_data = json.load(f)

for i in category_data:
    with open(f"../data/categories/{i}/index.json", "r") as f:
        CATEGORIES[i] = json.load(f)

    BATCHES[category_data[i]["link"]] = set()


# -----------------------------------------------------------------------------------
# Delete category index files
dir_path = "../categories/"
try:
    shutil.rmtree(dir_path)
except OSError as e:
    print("Error: %s : %s" % (dir_path, e.strerror))

# Delete project files
dir_path = "../projects/github_projects/"
try:
    shutil.rmtree(dir_path)
except OSError as e:
    print("Error: %s : %s" % (dir_path, e.strerror))

# -----------------------------------------------------------------------------------
# Download the repository data
repo_dict = {}
for p in range(1, 1000):
    url = (
        f"https://api.github.com/orgs/{ORGANIZATION}/repos?"
        f"per_page={RESULTS_PER_PAGE}&page={p}"
    )
    response = requests.get(url)

    if response.status_code == 200:
        jsonData = response.json()
        if len(jsonData) == 0:
            break

        for repo in jsonData:
            repo_dict[repo["name"]] = repo

    else:
        # TODO: Test
        errorMsg = f"An exception occurred while getting data from GitHub: {response.status_code}"
        print(">> Error:", errorMsg)
        notify.warning(errorMsg)

# -----------------------------------------------------------------------------------
# Write the repository data to a local source
# cache_file_path = "./__cache/repos.json"
# os.makedirs(os.path.dirname(cache_file_path), exist_ok=True)
# with open(cache_file_path, "w") as f:
#     json.dump(repo_dict, f, indent=4)

# -----------------------------------------------------------------------------------
# Read the repository data from a local source
# with open('./__cache/repos.json', 'r') as f:
#     repo_dict = json.load(f)


# -----------------------------------------------------------------------------------
# Iterate through the repositories in the GitHub
count = 0
for k in repo_dict:
    r = repo_dict[k]

    try:
        r_name = r["name"].strip().split("-")

        # Exclude the repository by definition
        isExcludedRepo = r["name"] in excludedReposList

        # Exclude duplicated / self-forked repositories
        if str(r_name[-1]).isdigit() and "-".join(r_name[:-1]) in repo_dict:
            print(f">> Error: Duplicate repository | {r['name']}")
            isExcludedRepo = True

        # General eligibility check to be a Student Project
        if (
            r_name[0][0] == "e"
            and r_name[0][1:].isdigit()
            and len(r_name) > 2
            and not isExcludedRepo
        ):
            batch = f"e{int(r_name[0][1:]):02d}"
            cat = r_name[1].lower()
            title = " ".join(r_name[2:])
            filename = "-".join(r_name[2:])
            count += 1

            print(f">> {cat} > {batch} > {title} ")

            # Check about whether the project belong to any allowed prohect category
            if cat in CATEGORIES:
                cat_name = CATEGORIES[cat]["title"]
                cat_cover = CATEGORIES[cat]["images"]["cover"]
                cat_thumb = CATEGORIES[cat]["images"]["thumbnail"]

                gh_page = (
                    f"https://cepdnaclk.github.io/{r['name']}"
                    if r["has_pages"]
                    else "blank"
                )
                desc = (
                    r["description"].strip().replace('"', "'")
                    if r["description"]
                    else ""
                )
                cover_url, thumbnail_url = get_custom_media(
                    default_cover=f"/data/categories/{cat}/{cat_cover}",
                    default_thumb=f"/data/categories/{cat}/{cat_thumb}",
                    gh_page=gh_page,
                )

                data = {
                    "layout": "project_page",
                    "title": title,
                    "permalink": f"/{cat}/{batch}/{filename}/",
                    "description": str(desc),
                    "has_children": False,
                    "parent": f"{batch.upper()} {cat_name}",
                    "grand_parent": cat_name,
                    "cover_url": cover_url,
                    "thumbnail_url": thumbnail_url,
                    "repo_url": r["html_url"],
                    "page_url": gh_page,
                    "forks": r["forks_count"],
                    "watchers": r["watchers_count"],
                    "stars": r["stargazers_count"],
                    "started_on": r["created_at"],
                }
                description = desc.replace('"', "'")

                # Write the project file
                path = f"../projects/github_projects/{cat}/{batch}/{filename}.md"
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w+", encoding="utf-8") as f:
                    f.write("---\n")
                    f.write(yaml.dump(data, sort_keys=False))
                    f.write("---\n\n")
                    f.write(description)

                BATCHES[cat].add(batch)

            else:
                print(f">> Error: Not belonged to a category | {r['name']}")

    except (KeyError, ValueError, OSError, requests.RequestException) as e:
        errorMsg = f"Repository processing failed for {r.get('name', '<unknown>')}: {type(e).__name__}"
        print(">> Error:", errorMsg, e)
        notify.warning(errorMsg, str(e))

print(f">> Created {count} repositories")

# -----------------------------------------------------------------------------------
# Generate the index files

id = 0
for cat in sorted(BATCHES):
    cat_data = CATEGORIES[cat]
    readmore_link = cat_data["readmore"] if ("readmore" in cat_data) else "#"

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
        "readmore": readmore_link,
        "default_thumb_image": f"/data/categories/{cat}/{cat_data['images']['thumbnail']}",
        "description": cat_data["description"],
    }
    id += 1

    # Write the category index file
    try:
        print(">> Write category index for", cat)
        path = "../categories/" + str(cat) + "/index.md"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write("---\n")
            f.write(yaml.dump(index_file, sort_keys=False))
            f.write("---\n")

    except Exception as e:
        errorMsg = f"An exception occurred while writing index file for {cat}"
        print(">> Error:", errorMsg, str(e))
        notify.warning(errorMsg, str(e))

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
            "readmore": readmore_link,
            "search_exclude": True,
            "default_thumb_image": f"/data/categories/{cat}/{cat_data['images']['thumbnail']}",
            "description": cat_data["description"],
        }

        try:
            path = f"../categories/{cat_data['code']}/{batch}.md"
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f2:
                f2.write("---\n")
                f2.write(yaml.dump(batch_file, sort_keys=False))
                f2.write("---\n")

        except Exception as e:
            errorMsg = (
                f"An exception occurred while writing index file for {cat}/{batch}"
            )
            print(">> Error:", errorMsg, str(e))
            notify.warning(errorMsg, str(e))

print(f">> Created {id} categories")

print("END")
