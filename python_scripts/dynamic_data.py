import requests
import os
import json

# NOTE
# The get_githubData() function call will be limited by the GitHub API's hourly quota.
# More: https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting

def get_tagData():
    tags_source = "https://api.ce.pdn.ac.lk/projects/v1/filter/tags/"

    req_tags = requests.get(tags_source)
    if req_tags.status_code==200:
        tag_data = json.loads(req_tags.text)

        # print(json.dumps(tag_data, indent = 4))

        print('\nTAGS:')
        for tag in tag_data:
            proj_count = len(tag_data[tag])

            if(proj_count>1):
                print(tag, proj_count)

        return tag_data
    else:
        return {}

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

        if("message" in jsonData):
            print(jsonData['message'])
            return {}

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
                    thumb_url = 'https://projects.ce.pdn.ac.lk/data/categories/{}/thumbnail.jpg'.format(cat)
                    formattedName = " ".join(repoName[2:])

                    proj_data[projName] = {
                        "projName": formattedName,
                        "batch": batch.upper(),
                        "category": CATEGORIES[cat]['name'],
                        "repo_url": jsonData[i]["html_url"],
                        "project_url": proj_url,
                        "page_url": jsonData[i]["homepage"],
                        "api_url": jsonData[i]["url"],
                        "thumb_url": thumb_url,
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
projects_gh = get_githubData()
projects_api = requests.get('https://api.ce.pdn.ac.lk/projects/v1/all/').json()
projects = {}
sorted_projects = {}

# print(json.dumps(projects_gh, indent = 4))

# merge with the data from the API site
for p in projects_gh:
    proj = projects_gh[p]

    if (p in projects_api):
        p_api = projects_api[p]
        proj['description'] = p_api['description']
        proj['category'] = p_api['category']
        proj['project_url'] = p_api['project_url']
        proj['repo_url'] = p_api['repo_url']
        proj['page_url'] = p_api['page_url']

        proj['team'] = p_api['team'] if ('team' in p_api) else {}
        proj['supervisors'] = p_api['supervisors'] if ('supervisors' in p_api) else {}
        proj['tags'] = p_api['tags'] if ('tags' in p_api) else {}

    projects[p] = proj

# Sort the projects data
for key in sorted(projects):
    sorted_projects[key] = projects[key]

# Write project data into file
filename = "../_data/projects.json"
os.makedirs(os.path.dirname(filename), exist_ok=True)
with open(filename, "w") as f:
    f.write(json.dumps(sorted_projects, indent = 4))

# Update Tag Data --------------------------------------------------------------
tags = get_tagData()

filename = "../_data/tags.json"
os.makedirs(os.path.dirname(filename), exist_ok=True)
with open(filename, "w") as f:
    f.write(json.dumps(tags, indent = 4))
