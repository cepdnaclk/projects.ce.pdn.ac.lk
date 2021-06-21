'''
    REQUIREMENTS:
        pip install requests

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

CATEGORIES = {}
BATCHES = {}
# url = 'https://api.github.com/repos/cepdnaclk/projects/git/blobs/2166c8eba0801b62b539a23576a7b6fc46e7f4f7'
# resp = requests.get(url)
# #print(resp)
# data = json.loads(resp.text)
# #print(data)
# #print(data['content'])
#
# message_bytes = base64.b64decode(data['content'])
# message = json.loads(message_bytes.decode('ascii'))

url = 'data/categories/index.json'
with open(url, 'r') as f:
    message = json.load(f)

for i in message:
    CATEGORIES[message[i]['link']] = message[i]['name']
    BATCHES[message[i]['link']] = set()
    # print(message[i]['link'])

print(CATEGORIES)

ORGANIZATION = "cepdnaclk"
PROJECTS = []
LOWERCASE = ['a', 'and', 'of', 'for', 'the', 'as', 'at', 'by', 'on', 'per', 'to', 'up', 'via', 'with', 'from' ]

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
    s = """---
layout: project_page
title: """ + title + """
permalink: """ + permalink + """
description: \"""" + description + """\"

has_children: false
parent: """ + batch.upper() + " " + grand_parent + """
grand_parent: """ + grand_parent + """

cover_url: /data/categories/""" + category + """/cover_page.jpg
thumbnail_url: /data/categories/""" + category + """/thumbnail.jpg

repo_url: """ + repo + """
page_url: """ + page + """

forks: """ + str(forks) + """
watchers: """ + str(watch) + """
stars: """ + str(stars) + """
started_on: """ + date + """
---
""" + description.replace("\"", "'") + """

"""
    return s


def batch_index_template(code, batch, tag, project, description):
    template = """---
layout: project_batch
title: E""" + batch + """ """ + project + """
permalink: /""" + tag + """/e""" + batch + """/
has_children: true
parent: """ + project + """
batch: e""" + batch + """
code: """ + code + """

search_exclude: true
default_thumb_image: /data/categories/""" + tag + """/thumbnail.jpg
description: """ + description
    return template


def index_template(id, code, title, cover, thumbnail, description, contact, type):
    template = """---
layout: project_cat
title: """ + title + """
nav_order: """ + str(id) + """
permalink: /""" + code + """/
has_children: true

code: """ + code + """
type: """ + type + """
parent: Home
has_toc: true
search_exclude: true

default_thumb_image: /data/categories/""" + code + """/""" + thumbnail + """
description: """ + description + """
---"""
    return template


def md_file_write(CATEGORIES, BATCHES):
    for i in CATEGORIES:
        index = open("docs/categories/" + str(i) + "/index.md", 'r')
        index_data = index.read()

        for batch in BATCHES[i]:
            batch_str = str(batch)
            if batch < 10:
                batch_str = '0' + batch_str
            filename = 'e' + batch_str

            path = "docs/categories/" + str(i) + "/" + filename + ".md"

            os.makedirs(os.path.dirname(path), exist_ok=True)
            outputFile = open(path, "w+")
            outputFile.write(
                batch_index_template(str(i), batch_str, str(i), CATEGORIES[i], index_data.split("description: ", 1)[1]))


def index_files(CATEGORIES):
    id = 0
    for i in CATEGORIES:
        index = open("data/categories/" + str(i) + "/index.json", 'r')
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

        path = "docs/categories/" + str(i) + "/index.md"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        outputFile = open(path, "w+")
        id += 1
        outputFile.write(index_template(id, code, title, cover, thumbnail, description, contact, categoryType))


def del_docs_categories():
    dir_path = "docs/categories/"
    try:
        shutil.rmtree(dir_path)
    except OSError as e:
        print("Error: %s : %s" % (dir_path, e.strerror))


def del_docs_github_repos():
    dir_path = "docs/github_projects/"
    try:
        shutil.rmtree(dir_path)
    except OSError as e:
        print("Error: %s : %s" % (dir_path, e.strerror))


if __name__ == "__main__":
    print("START")
    URL = urlOrganization()

    # No need to delete categpries files,
    # because this is always increasing, and some batch files were created manually
    # del_docs_categories()
    del_docs_github_repos()

    r = requests.get(url=URL)
    j = r.json()

    for p in range(1, 1000):
        r = requests.get(url=urlOrganizationRepos(p))
        jsonData = r.json()
        # print(urlOrganizationRepos(p))
        # sleep(60)

        # print(p, jsonData)
        # print("\n\n\n")

        if len(jsonData) == 0:
            break

        for i in range(len(jsonData)):
            print(jsonData[i]["name"])
            repoName = jsonData[i]["name"].strip().split("-")

            if len(repoName)>1 and repoName[0][0] == "e" and repoName[0][1:] != 'YY':
                if repoName[1] in CATEGORIES:
                    try:
                        batch = int(repoName[0][1:])
                        BATCHES[repoName[1]].add(batch)
                        filename = '-'.join(repoName[2:])
                        path = "docs/github_projects/" + repoName[1] + "/" + repoName[0] + "/" + filename + ".md"
                        title = []
                        title = ' '.join(repoName[2:]).split()

                        # TODO: move this into a separate function

                        capitalized = ' '.join(repoName[2:])
                        # capitalized = "" # title[0].capitalize()
                        # for ii in range(0, len(title)):
                        #     word = title[ii]
                        #
                        #     if word == word.upper():
                        #         # already in upper case
                        #         capitalized = capitalized + " " + word
                        #
                        #     elif word in LOWERCASE:
                        #         # and, for, a kind of words
                        #         capitalized = capitalized + " " + word
                        #
                        #     else:
                        #         # capitalized = capitalized + " " + word.capitalize()
                        #         capitalized = capitalized + " " + word

                        print(capitalized)

                        permalink = "/" + repoName[1] + "/" + repoName[0] + "/" + filename
                        stars = jsonData[i]["stargazers_count"]
                        forks = jsonData[i]["forks_count"]
                        watch = jsonData[i]["watchers_count"]
                        date = jsonData[i]["created_at"]
                        repo = "https://github.com/cepdnaclk/" + '-'.join(repoName)

                        if jsonData[i]["has_pages"]:
                            page = "https://cepdnaclk.github.io/" + '-'.join(repoName)
                        else:
                            page = "blank"

                        os.makedirs(os.path.dirname(path), exist_ok=True)
                        outputFile = open(path, "w+", encoding="utf-8")

                        if jsonData[i]["description"]:
                            desc = jsonData[i]["description"]
                        else:
                            desc = ''

                        if repoName[1] in CATEGORIES:
                            grand_parent = CATEGORIES[repoName[1]]
                        else:
                            grand_parent = 'xxx'

                        outputFile.write(
                            writeHeader(repoName[1], repoName[0], grand_parent, permalink, capitalized, desc, stars, forks, watch, date, repo, page))

                    except Exception as e:
                        print("\tAn exception occurred on", jsonData[i]["name"])
                        print(e.__class__, "occurred.")
                        print(traceback.format_exc())


        print(BATCHES)
        index_files(CATEGORIES)
        md_file_write(CATEGORIES, BATCHES)

print("END")
