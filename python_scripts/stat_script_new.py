'''
REQUIREMENTS:
    pip install requests
    pip install pyyaml

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

CATEGORIES = {}
BATCHES = {}

url = '../data/categories/index.json'
with open(url, 'r') as f:
    category_data = json.load(f)

for i in category_data:
    # CATEGORIES[i] = category_data[i]['name']

    with open("../data/categories/{}/index.json".format(i), 'r') as f:
        CATEGORIES[i] = json.load(f)

    BATCHES[category_data[i]['link']] = set()

# print(CATEGORIES)

ORGANIZATION = "cepdnaclk"
RESULTS_PER_PAGE = 100

projects = []


def md_file_write(CATEGORIES, batch_map):
    id = 0
    for code in batch_map:
        data = CATEGORIES[code]
        readmore_link = data['readmore'] if ('readmore' in data) else '#'

        index_file = {
            'layout': "project_cat",
            'title': data['title'],
            'nav_order': str(id),
            'permalink': "/{}/".format(code),
            'has_children': True,
            'code': data['code'],
            'type': data['type'],
            'parent': "Home",
            'has_toc': True,
            'search_exclude': True,
            'readmore': readmore_link,
            'default_thumb_image': "/data/categories/{}/{}".format(data['code'], data['images']['thumbnail']),
            'description': data['description'],
        }

        id += 1
        path = "../categories/" + str(code) + "/index.md"
        os.makedirs(os.path.dirname(path), exist_ok=True)

        print(">> Write category index for", code)
        with open(path, "w") as f:
            f.write('---\n')
            f.write(yaml.dump(index_file, sort_keys=False))
            f.write('---\n')

        for batch in batch_map[code]:
            batch_file = {
                'layout': "project_batch",
                'title': "E{} {}".format(batch[1:], CATEGORIES[code]['title']),
                'permalink': "/{}/{}/".format(code, batch),
                'has_children': True,
                'parent': CATEGORIES[code]['title'],
                'batch': batch,
                'code': str(code),
                'readmore': readmore_link,
                'search_exclude': True,
                'default_thumb_image': "/data/categories/{}/{}".format(code, data['images']['thumbnail']),
                'description': data['description'],
            }

            path = "../categories/{}/{}.md".format(code, batch)
            os.makedirs(os.path.dirname(path), exist_ok=True)

            print("\t", batch)
            with open(path, "w") as f2:
                f2.write('---\n')
                f2.write(yaml.dump(batch_file, sort_keys=False))
                f2.write('---\n')


def del_old_files():
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


print("START")

del_old_files()

# # Download the repository data
# repo_list = []
# for p in range(1, 1000):
#     url = "https://api.github.com/orgs/{}/repos?per_page={}&page={}".format(
#         ORGANIZATION, RESULTS_PER_PAGE, p)
#     response = requests.get(url)

#     if response.status_code == 200:
#         jsonData = response.json()
#         if len(jsonData) == 0:
#             break

#         repo_list.extend(jsonData)
#     else:
#         # TODO: Handle error
#         print("ERROR:", reponse.status_code)

# with open("repos.json", "w") as f:
#     json.dump(repo_list, f, indent=4)

# -----------------------------------------------------------------------------------
# Read the repository data from a local source
with open('./repos.json', 'r') as f:
    repo_list = json.load(f)

# -----------------------------------------------------------------------------------
count = 0

for r in repo_list:
    try:
        r_name = r['name'].strip().split('-')

        if r_name[0][0] == 'e' and r_name[0][1:].isdigit() and len(r_name) > 2:
            batch = "e{:02}".format(int(r_name[0][1:]))
            cat = r_name[1].lower()
            title = ' '.join(r_name[2:])
            filename = '-'.join(r_name[2:])
            count += 1

            if cat in CATEGORIES:
                cat_name = CATEGORIES[cat]['title']
                cat_cover = CATEGORIES[cat]['images']['cover']
                cat_thumb = CATEGORIES[cat]['images']['thumbnail']

                # print(batch, cat, title)
                gh_page = "https://cepdnaclk.github.io/{}".format(
                    r['name']) if r["has_pages"] else 'blank'

                path = "../projects/github_projects/{}/{}/{}.md".format(
                    cat, batch, filename)

                desc = r["description"].strip().replace(
                    "\"", "'") if r["description"] else ''

                os.makedirs(os.path.dirname(path), exist_ok=True)

                data = {
                    'layout': "project_page",
                    'title': title,
                    'permalink': "/{}/{}/{}/".format(cat, batch, filename),
                    'description': str(desc),
                    'has_children': False,
                    'parent': "E{} {}".format(batch.upper(), cat_name),
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

                with open(path, "w+", encoding="utf-8") as f:
                    f.write("---\n")
                    f.write(yaml.dump(data, sort_keys=False))
                    f.write("---\n\n")
                    f.write(description)

                # TODO: Update batch/cat files
                BATCHES[cat].add(batch)

            else:
                # TODO: Handle error
                print(">> Error: not belonged to a category",  r['name'])

    except Exception as e:
        # TODO: Notify in the Discord Channel with message
        a = 1
        # print(">> An exception occurred with:", r["name"], e)

print(">> Downloaded {} repositories".format(count))

print(BATCHES)
md_file_write(CATEGORIES, BATCHES)

print("END")
