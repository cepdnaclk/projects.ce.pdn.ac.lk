import requests
import os
import json


def get_tagData():
    tags_source = "https://api.ce.pdn.ac.lk/projects/v1/filter/tags/"

    req_tags = requests.get(tags_source)
    if req_tags.status_code==200:
        tag_data = json.loads(req_tags.text)

    # print(json.dumps(tag_data, indent = 4))

    for tag in tag_data:
        proj_count = len(tag_data[tag])

        if(proj_count>1):
            print(tag, proj_count)

    return tag_data

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

    for p in range(1, 1000):
        url = "https://api.github.com/orgs/{}/repos?page={}".format(org, p)
        # print(url)
        jsonData = requests.get(url).json()

        if len(jsonData) == 0:
            break

        for i in range(len(jsonData)):
            repoName = jsonData[i]["name"].strip().split("-")

            if len(repoName)>1 and repoName[0][0] == "e" and repoName[0][1:] != 'YY':
                if repoName[1] in CATEGORIES:
                    batch = repoName[0]
                    cat = repoName[1]
                    name = "-".join(repoName[2:])
                    projName = jsonData[i]["name"]
                    print(projName)

                    proj_url = 'https://projects.ce.pdn.ac.lk/{}/{}/{}'.format(cat, batch.lower(), name)

                    proj_data[projName] = {
                        "repo_url": jsonData[i]["html_url"],
                        "project_url": proj_url,
                        "page_url": jsonData[i]["homepage"],
                        "api_url": jsonData[i]["url"],
                        "created_at": jsonData[i]["created_at"],
                        "updated_at": jsonData[i]["updated_at"],
                        "forks_count": jsonData[i]["forks_count"],
                        "stars_count": jsonData[i]["stargazers_count"],
                        "watchers_count": jsonData[i]["watchers_count"],
                        "language": jsonData[i]["language"],
                        "topics": jsonData[i]["topics"],
                        "has_projects": jsonData[i]["has_projects"],
                        "has_wiki": jsonData[i]["has_wiki"],
                        "has_pages": jsonData[i]["has_pages"],
                    }

    return proj_data

# Update Project Data ----------------------------------------------------------
projects = get_githubData()

# Write project data into file
filename = "../_data/projects.json"
os.makedirs(os.path.dirname(filename), exist_ok=True)
with open(filename, "w") as f:
    f.write(json.dumps(projects, indent = 4))

# Update Tag Data ----------------------------------------------------------
tags = get_tagData()

# Write project data into file
filename = "../_data/tags.json"
os.makedirs(os.path.dirname(filename), exist_ok=True)
with open(filename, "w") as f:
    f.write(json.dumps(tags, indent = 4))
