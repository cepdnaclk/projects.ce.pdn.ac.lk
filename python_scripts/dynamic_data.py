'''
REQUIREMENTS:
    pip install requests

AUTHORS:
    Nuwan Jaliyagoda
'''

import requests
import os
import json

from notifications import Notifications

notify = Notifications("projects.ce.pdn.ac.lk", "Generate Dynamic Data")

# NOTE
# The get_githubData() function call will be limited by the GitHub API's hourly quota.
# More: https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting

ORGANIZATION = "cepdnaclk"
RESULTS_PER_PAGE = 100

excludedReposList = [
    "e03-final-year-projects",
    "e04-final-year-projects",
    "e05-final-year-projects"
]

def get_categories():
    CATEGORIES = {}
    url = '../data/categories/index.json'
    with open(url, 'r') as f:
        data = json.load(f)

    return data


def get_githubData():

    org = "cepdnaclk"
    CATEGORIES = get_categories()
    proj_data = {}

    # -------------------------------------------------------------------------
    # Download the repository data
    repo_dict = {}
    for p in range(1, 1000):
        url = "https://api.github.com/orgs/{}/repos?per_page={}&page={}".format(
            ORGANIZATION, RESULTS_PER_PAGE, p)
        response = requests.get(url)

        if response.status_code == 200:
            jsonData = response.json()
            if len(jsonData) == 0:
                break

            for repo in jsonData:
                repo_dict[repo['name']] = repo

        else:
            # TODO: Test
            errorMsg = "An exception occurred while getting data from GitHub: {}".format(
                reponse.status_code)
            print(">> Error:", errorMsg)
            notify.warning(errorMsg)
            

    for k in repo_dict:
        r = repo_dict[k]
        r_name = r['name'].strip().split('-')

        # Exclude the repository by definition
        isExcludedRepo = r['name'] in excludedReposList

        # Exclude duplicated / self-forked repositories
        if str(r_name[-1]).isdigit() and "-".join(r_name[:-1]) in repo_dict:
            print(">> Error: Duplicate repository | {}".format(r['name']))
            isExcludedRepo = True

        repoName = r["name"].strip().split("-")

        # General eligibility check to be a Student Project
        if r_name[0][0] == 'e' and r_name[0][1:].isdigit() and len(r_name) > 2 and not isExcludedRepo:
            if repoName[1] in CATEGORIES:
                batch = repoName[0]
                cat = repoName[1]
                name = "-".join(repoName[2:])
                projName = r["name"]
                print(">>", projName)

                proj_url = 'https://projects.ce.pdn.ac.lk/{}/{}/{}'.format(
                    cat, batch.lower(), name)
                thumb_url = 'https://projects.ce.pdn.ac.lk/data/categories/{}/thumbnail.jpg'.format(
                    cat)
                formattedName = " ".join(repoName[2:])

                proj_data[projName] = {
                    "projName": formattedName,
                    "batch": batch.upper(),
                    "category": CATEGORIES[cat]['name'],
                    "repo_url": r["html_url"],
                    "project_url": proj_url,
                    "page_url": r["homepage"],
                    "api_url": r["url"],
                    "thumb_url": thumb_url,
                    "created_at": r["created_at"],
                    "updated_at": r["updated_at"],
                    "forks_count": r["forks_count"],
                    "stars_count": r["stargazers_count"],
                    "watchers_count": r["watchers_count"],
                    "language": r["language"],
                    "topics": r["topics"],
                    "has_projects": r["has_projects"],
                    "has_wiki": r["has_wiki"],
                    "has_pages": r["has_pages"],
                }

    return proj_data


# Update Project Data ----------------------------------------------------------
projects_gh = get_githubData()
projects_api = requests.get('https://api.ce.pdn.ac.lk/projects/v1/all/').json()
projects = {}
sorted_projects = {}

# Merge with the data from the API site ----------------------------------------
for p in projects_gh:
    proj = projects_gh[p]

    if (p in projects_api):
        p_api = projects_api[p]

        # replace \u2019 with ' in description
        p_api['description'] = p_api['description'].replace('\u2019', "'")
        # remove emojis from description
        p_api['description'] = p_api['description'].encode('ascii', 'ignore').decode('ascii')
        
        proj['description'] = p_api['description']
        proj['category'] = p_api['category']
        proj['project_url'] = p_api['project_url']
        proj['repo_url'] = p_api['repo_url']
        proj['page_url'] = p_api['page_url']

        proj['team'] = p_api['team'] if ('team' in p_api) else {}
        proj['supervisors'] = p_api['supervisors'] if ('supervisors' in p_api) else {}
        proj['tags'] = p_api['tags'] if ('tags' in p_api) else {}

    projects[p] = proj

# Sort the projects data -------------------------------------------------------
for key in sorted(projects):
    sorted_projects[key] = projects[key]

# Write project data into file -------------------------------------------------
filename = "../_data/projects.json"
os.makedirs(os.path.dirname(filename), exist_ok=True)
with open(filename, "w") as f:
    f.write(json.dumps(sorted_projects, indent=4))

# Update Tag Data --------------------------------------------------------------
tags_source = "https://api.ce.pdn.ac.lk/projects/v1/filter/tags/"
tags = {}

req_tags = requests.get(tags_source)
if req_tags.status_code == 200:
    tags = json.loads(req_tags.text)
    print('\nTAGS:')
    for tag in tags:
        proj_count = len(tags[tag])

        if (proj_count > 1):
            print('\t', proj_count, tag)

filename = "../_data/tags.json"
os.makedirs(os.path.dirname(filename), exist_ok=True)
with open(filename, "w") as f:
    f.write(json.dumps(tags, indent=4))
