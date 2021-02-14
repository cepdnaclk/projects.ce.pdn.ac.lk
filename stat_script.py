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
from datetime import datetime
import re, json
import base64

CATEGORIES={}

url = 'data/categories/index.json'
with open(url, 'r') as f:
    message = json.load(f)

# message = resp.json()

for i in message:
    CATEGORIES[message[i]['link']] = message[i]['name']

print(CATEGORIES)

ORGANIZATION = "cepdnaclk"
PROJECTS = []
LOWERCASE = ['a','and','of','for','the','as','at','by','on','per','to','up','via','with','from']

MIN = 100
MAX = 0

def urlOrganization():
    return "https://api.github.com/orgs/{}".format(ORGANIZATION)


def urlOrganizationRepos(pageNo):
    return "https://api.github.com/orgs/{}/repos?page={}".format(ORGANIZATION, pageNo)


# def inRange(x, minNumber, maxNumber):
#     if type(x) == str:
#         x = int(x)
#     if minNumber > maxNumber:
#         minNumber, maxNumber = maxNumber, minNumber
#     if minNumber <= x and maxNumber >= x:
#         return True
#     else:
#         return False


def writeHeader(category,batch,grand_parent,permalink,title,description,stars,forks,watch,date,repo,page):
    s = """---
layout: project_page
title: """+title.title()+"""
permalink: """+permalink+"""
description: \""""+description+"""\"

has_children: false
parent: """+batch.upper()+ " " + grand_parent + """
grand_parent: """+grand_parent+"""

cover_url: /data/categories/"""+category+"""/cover_page.jpg
thumbnail_url: /data/categories/"""+category+"""/thumbnail.jpg

repo_url: """+repo+"""
page_url: """+page+"""

forks: """+str(forks)+"""
watchers: """+str(watch)+"""
stars: """+str(stars)+"""
started_on: """+date+"""
---
"""+description+"""

"""
    return s


def index_template(batch,tag,project,description):
    template = """---
layout: project_batch
title: E"""+batch+""" """+project+"""
permalink: /"""+tag+"""/e"""+batch+"""
has_children: true
parent: """+project+"""
batch: e"""+batch.rjust(2, '0')+"""

default_thumb_image: /data/categories/"""+tag+"""/thumbnail.jpg
description: """+description

    return template

def md_batch_file_write(CATEGORIES,MIN,MAX):
    print(MIN, MAX)

    for i in CATEGORIES:
        index = open("docs/categories/"+str(i).rjust(2, '0')+"/index.md",'r')
        index_data = index.read()
        print(i)

        for batch in range(MIN,MAX+1):
            filename = 'e'+str(batch)
            path = "docs/categories/"+str(i)+"/"+filename+".md"
            os.makedirs(os.path.dirname(path), exist_ok=True)
            outputFile = open(path, "w+")
            outputFile.write(index_template(str(batch),str(i),CATEGORIES[i],index_data.split("description: ",1)[1]))

if __name__ == "__main__":
    print("START")
    URL = urlOrganization()

    # TODO:
    # Delete the files on docs/github_repos/

    r = requests.get(url=URL)
    j = r.json()

    for p in range(1, 1000):

        r = requests.get(url=urlOrganizationRepos(p))
        jsonData = r.json()

        if len(jsonData) == 0:
            break

        #removed if condition for checking year and batch in range
        for i in range(len(jsonData)):
            # print(jsonData[i]["name"])
            repoName = jsonData[i]["name"].strip().split("-")

            if repoName[0][0] == "e" and repoName[0][1:] != 'YY':
                if repoName[1] in CATEGORIES:
                    # print(repoName)
                    # if(repoName[1][:1]=='c'):
                    #     year = int(repoName[1][2])
                    # else:
                    #     year = int(repoName[1][:1])

                    batch = int(repoName[0][1:])

                    if(batch<MIN):
                        MIN = batch
                    if(batch>MAX):
                        MAX = batch

                    filename = '-'.join(repoName[2:])

                    path = "docs/github_repos/"+repoName[1]+"/" + repoName[0]+"/"+filename+".md"
                    title = []
                    title = ' '.join(repoName[2:]).split()

                    capitalized = title[0].capitalize()
                    for i in range(1,len(title)):
                        word = title[i]
                        if word not in LOWERCASE:
                            capitalized = capitalized + " "+ word.capitalize()
                        else:
                            capitalized = capitalized +" " + word
                    print(capitalized)

                    permalink = "/"+repoName[1]+"/" + repoName[0]+"/"+filename
                    stars = jsonData[i]["stargazers_count"]
                    forks = jsonData[i]["forks_count"]
                    watch = jsonData[i]["watchers_count"]
                    date = jsonData[i]["created_at"]
                    repo = "https://github.com/cepdnaclk/"+'-'.join(repoName)

                    if jsonData[i]["has_pages"]:
                        page = "https://cepdnaclk.github.io/"+'-'.join(repoName)
                    else:
                        page = "blank"

                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    outputFile = open(path, "w+")

                    if jsonData[i]["description"]:
                        desc = jsonData[i]["description"]
                    else:
                        desc = ''

                    if repoName[1] in CATEGORIES:
                        grand_parent = CATEGORIES[repoName[1]]
                    else:
                        grand_parent = 'xxx'

                    outputFile.write(writeHeader(repoName[1],repoName[0],grand_parent,permalink,capitalized,desc,stars,forks,watch,date,repo,page))

                else:
                    # print('category not found:', jsonData[i]["name"])

    md_batch_file_write(CATEGORIES,MIN,MAX)

print("END")
