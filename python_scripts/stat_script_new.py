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


def urlOrganization():
    return "https://api.github.com/orgs/{}".format(ORGANIZATION)


def urlOrganizationRepos(pageNo):
    return "https://api.github.com/orgs/{}/repos?page={}".format(ORGANIZATION, pageNo)


def inRange(x, minNumber, maxNumber):
    if type(x) == str:
        x = int(x)
    if minNumber > maxNumber:
        minNumber, maxNumber = maxNumber, minNumber
    if minNumber <= x and maxNumber >= x:
        return True
    else:
        return False


def writeHeader(category, batch, grand_parent, permalink, title, description, stars, forks, watch, date, repo, page):
    data = {
        'layout': "project_page",
        'title': title,
        'permalink': permalink,
        'description': description,
        'has_children': False,
        'parent': "{} {}".format(batch.upper(), grand_parent),
        'grand_parent': grand_parent,
        'cover_url': "/data/categories/{}/cover_page.jpg".format(category),
        'thumbnail_url': "/data/categories/{}/thumbnail.jpg".format(category),
        'repo_url': repo,
        'page_url': page,
        'forks': str(forks),
        'watchers': str(watch),
        'stars': str(stars),
        'started_on': date
    }
    desc = description.replace("\"", "'")
    return "---\n{}\n---\n\n{}\n\n".format(yaml.dump(data, sort_keys=False), desc)


def batch_index_template(code, batch, tag, project, description, readmore_link='#'):
    data = {
        'layout': "project_batch",
        'title': "E{} {}".format(batch, project),
        'permalink': "/{}/e{}/".format(tag, batch),
        'has_children': True,
        'parent': project,
        'batch': "e{}".foramt(batch),
        'code': code,
        'readmore': readmore_link,
        'default_thumb_image': "/data/categories/{}/{}".format(code, thumbnail),
        'description': description,
        'search_exclude': True
    }
    return yaml.dump(data, sort_keys=False)


def index_template(id, code, title, cover, thumbnail, description, contact, proj_type, readmore_link="#"):
    data = {
        'layout': "project_cat",
        'title': title,
        'nav_order': str(id),
        'permalink': "/{}/".format(code),
        'has_children': True,
        'code': code,
        'type': proj_type,
        'parent': "Home",
        'has_toc': True,
        'search_exclude': True,
        'readmore': readmore_link,
        'default_thumb_image': "/data/categories/{}/{}".format(code, thumbnail),
        'description': description,
    }
    return yaml.dump(data, sort_keys=False)


def md_file_write(CATEGORIES, BATCHES):
    for code in CATEGORIES:
        index = open("../data/categories/{}/index.json".fomat(i), 'r')
        index_data = index.read()
        data = json.loads(index_data)

        description = data['description']
        readmore_link = data['readmore'] if ('readmore' in data) else '#'

        for batch in BATCHES[code]:
            # batch_str = str(batch)
            # if batch < 10:
            #     batch_str = '0' + batch_str
            filename = "e{:02}".foramt(batch)

            outputFile = open(path, "w+")
            # code, batch, tag, project, description, readmore_link='#'
            # outputFile.write(batch_index_template(code=str(i), batch=batch_str, tag=str(i), CATEGORIES[i], description, readmore_link))

            project = CATEGORIES[code]
            data = {
                'layout': "project_batch",
                'title': "E{} {}".format(batch, project),
                'permalink': "/{}/e{}/".format(code, batch),
                'has_children': True,
                'parent': project,
                'batch': "e{:02}".foramt(batch),
                'code': str(code),
                'readmore': readmore_link,
                'default_thumb_image': "/data/categories/{}/{}".format(code, thumbnail),
                'description': description,
                'search_exclude': True
            }

            path = "../categories/{}/{}.md".format(code, filename)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                f.write('---')
                f.write(yaml.dump(data, sort_keys=False))
                f.write('---')


def index_files(CATEGORIES):
    id = 0
    for i in CATEGORIES:
        index = open("../data/categories/" + str(i) + "/index.json", 'r')
        index_data = index.read()
        data = json.loads(index_data)

        code = data['code']
        title = data['title']
        cover = data['images']['cover']
        thumbnail = data['images']['thumbnail']
        description = data['description']
        contact = data['contact']

        # course project or general
        categoryType = data['type']
        readmore_link = data['readmore'] if ('readmore' in data) else '#'

        path = "../categories/" + str(i) + "/index.md"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        outputFile = open(path, "w+")
        id += 1
        outputFile.write(index_template(id, code, title, cover,
                         thumbnail, description, contact, categoryType, readmore_link))


def del_docs_categories():
    dir_path = "../categories/"
    try:
        shutil.rmtree(dir_path)
    except OSError as e:
        print("Error: %s : %s" % (dir_path, e.strerror))


def del_docs_github_repos():
    dir_path = "../projects/github_projects/"
    try:
        shutil.rmtree(dir_path)
    except OSError as e:
        print("Error: %s : %s" % (dir_path, e.strerror))


print("START")

del_docs_github_repos()

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
            batch = "{:02}".format(int(r_name[0][1:]))
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

                path = "../projects/github_projects/{}/e{}/{}.md".format(
                    cat, batch, filename)

                desc = r["description"].strip().replace(
                    "\"", "'") if r["description"] else ''

                os.makedirs(os.path.dirname(path), exist_ok=True)

                data = {
                    'layout': "project_page",
                    'title': title,
                    'permalink': "/{}/e{}/{}/".format(cat, batch, filename),
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

            else:
                # TODO: Handle error
                print("not belonged to a category",  r['name'])

    except Exception as e:
        # TODO: Notify in the Discord Channel with message
        print(">> An exception occurred with:", r["name"], e)

print(">> downloaded {} repositories".format(count))
print("END")
