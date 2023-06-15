'''
REQUIREMENTS:
    pip install requests pyyaml

AUTHORS:
    Gihan Jayatilake
    Nuwan Jaliyagoda
    Akila Karunanayake
'''

import requests
import os
import json
import shutil
import traceback
import yaml

from notifications import Notifications

notify = Notifications("projects.ce.pdn.ac.lk",
                       "Daily_Site_python_scripts\__pycache__Builder")

CATEGORIES = {}
BATCHES = {}
ORGANIZATION = "cepdnaclk"
RESULTS_PER_PAGE = 100
excludedReposList = [
    "e03-final-year-projects",
    "e04-final-year-projects",
    "e05-final-year-projects"
]
projects = []

print("START")

# -----------------------------------------------------------------------------------
# Load Category data
url = '../data/categories/index.json'
with open(url, 'r') as f:
    category_data = json.load(f)

for i in category_data:
    with open("../data/categories/{}/index.json".format(i), 'r') as f:
        CATEGORIES[i] = json.load(f)

    BATCHES[category_data[i]['link']] = set()


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
repo_list = []
for p in range(1, 1000):
    url = "https://api.github.com/orgs/{}/repos?per_page={}&page={}".format(
        ORGANIZATION, RESULTS_PER_PAGE, p)
    response = requests.get(url)

    if response.status_code == 200:
        jsonData = response.json()
        if len(jsonData) == 0:
            break

        repo_list.extend(jsonData)
    else:
        # TODO: Test
        errorMsg = "An exception occurred while getting data from GitHub: {}".format(
            reponse.status_code)
        print(">> Error:", errorMsg)
        notify.warning(errorMsg)

# # -----------------------------------------------------------------------------------
# # Write the repository data to a local source
# cache_file_path = "./__cache/repos.json"
# os.makedirs(os.path.dirname(cache_file_path), exist_ok=True)
# with open(cache_file_path, "w") as f:
#     json.dump(repo_list, f, indent=4)

# # -----------------------------------------------------------------------------------
# # Read the repository data from a local source
# with open('./__cache/repos.json', 'r') as f:
#     repo_list = json.load(f)


# -----------------------------------------------------------------------------------
# Iterate through the repositories in the GitHub
count = 0
for r in repo_list:
    try:
        r_name = r['name'].strip().split('-')
        isExcludedRepo = r['name'] in excludedReposList

        # General eligibility check to be a Student Project
        if r_name[0][0] == 'e' and r_name[0][1:].isdigit() and len(r_name) > 2 and not isExcludedRepo:

            batch = "e{:02}".format(int(r_name[0][1:]))
            cat = r_name[1].lower()
            title = ' '.join(r_name[2:])
            filename = '-'.join(r_name[2:])
            count += 1

            # Check about whether the project belong to any allowed prohect category
            if cat in CATEGORIES:
                cat_name = CATEGORIES[cat]['title']
                cat_cover = CATEGORIES[cat]['images']['cover']
                cat_thumb = CATEGORIES[cat]['images']['thumbnail']

                gh_page = "https://cepdnaclk.github.io/{}".format(
                    r['name']) if r["has_pages"] else 'blank'
                desc = r["description"].strip().replace(
                    "\"", "'") if r["description"] else ''

                data = {
                    'layout': "project_page",
                    'title': title,
                    'permalink': "/{}/{}/{}/".format(cat, batch, filename),
                    'description': str(desc),
                    'has_children': False,
                    'parent': "{} {}".format(batch.upper(), cat_name),
                    'grand_parent': cat_name,
                    'cover_url': "/data/categories/{}/{}".format(cat, cat_cover),
                    'thumbnail_url': "/data/categories/{}/{}".format(cat, cat_thumb),
                    'repo_url': r['html_url'],
                    'page_url': gh_page,
                    'forks': r["forks_count"],
                    'watchers': r["watchers_count"],
                    'stars': r["stargazers_count"],
                    'started_on': r["created_at"]
                }
                description = desc.replace("\"", "'")

                # Write the project file
                path = "../projects/github_projects/{}/{}/{}.md".format(
                    cat, batch, filename)
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w+", encoding="utf-8") as f:
                    f.write("---\n")
                    f.write(yaml.dump(data, sort_keys=False))
                    f.write("---\n\n")
                    f.write(description)

                BATCHES[cat].add(batch)

            else:
                print(
                    ">> Error: {} is not belonged to a category".format(r['name']))

    except Exception as e:
        # TODO: Test
        errorMsg = "An exception occurred with {} :".format(r["name"])
        print(">> Error:", errorMsg, e)
        notify.warning(errorMsg, str(e))

print(">> Created {} repositories".format(count))

# -----------------------------------------------------------------------------------
# Generate the index files

id = 0
for cat in sorted(BATCHES):
    cat_data = CATEGORIES[cat]
    readmore_link = cat_data['readmore'] if ('readmore' in cat_data) else '#'

    index_file = {
        'layout': "project_cat",
        'title': cat_data['title'],
        'nav_order': str(id),
        'permalink': "/{}/".format(cat),
        'has_children': True,
        'code': cat,
        'type': cat_data['type'],
        'parent': "Home",
        'has_toc': True,
        'search_exclude': True,
        'readmore': readmore_link,
        'default_thumb_image': "/data/categories/{}/{}".format(cat, cat_data['images']['thumbnail']),
        'description': cat_data['description'],
    }
    id += 1

    # Write the category index file
    try:
        print(">> Write category index for", cat)
        path = "../categories/" + str(cat) + "/index.md"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write('---\n')
            f.write(yaml.dump(index_file, sort_keys=False))
            f.write('---\n')

    except Exception as e:
        errorMsg = "An exception occurred while writing index file for {}".format(
            cat)
        print(">> Error:", errorMsg, str(e))
        notify.warning(errorMsg, str(e))

    # Write batch index files for each batch under the category
    for batch in BATCHES[cat]:
        batch_file = {
            'layout': "project_batch",
            'title': "E{} {}".format(batch[1:], cat_data['title']),
            'permalink': "/{}/{}/".format(cat, batch),
            'has_children': True,
            'parent': cat_data['title'],
            'batch': batch,
            'code': str(cat),
            'readmore': readmore_link,
            'search_exclude': True,
            'default_thumb_image': "/data/categories/{}/{}".format(cat, cat_data['images']['thumbnail']),
            'description': cat_data['description'],
        }

        # Write the batch file
        try:
            # print("\t", batch)
            path = "../categories/{}/{}.md".format(cat_data['code'], batch)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f2:
                f2.write('---\n')
                f2.write(yaml.dump(batch_file, sort_keys=False))
                f2.write('---\n')

        except Exception as e:
            errorMsg = "An exception occurred while writing index file for {}/{}".format(
                cat, batch)
            print(">> Error:", errorMsg, str(e))
            notify.warning(errorMsg, str(e))

print(">> Created {} categories".format(id))

print("END")
