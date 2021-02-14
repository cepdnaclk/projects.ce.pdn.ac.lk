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

# message = resp.json()

for i in message:
    CATEGORIES[message[i]['link']] = message[i]['name']
    #print(message[i]['link'])

print(CATEGORIES)

ORGANIZATION = "cepdnaclk"
PROJECTS = []
LOWERCASE = ['a','and','of','for']
START_BATCH = 10
END_BATCH = 16
FIRST_YEAR = 2
FINAL_YEAR = 4

MIN = 10
MAX = 10


def urlOrganization():
    return "https://api.github.com/orgs/{}".format(ORGANIZATION)


def urlOrganizationRepos(pageNo):
    return "https://api.github.com/orgs/{}/repos?page={}".format(ORGANIZATION, pageNo)


def initialize():
    for batch in range(START_BATCH, END_BATCH+1):
        temp = []
        for year in range(FIRST_YEAR, FINAL_YEAR+1):
            temp.append([])
        PROJECTS.append(temp)


def inRange(x, minNumber, maxNumber):
    if type(x) == str:
        x = int(x)
    if minNumber > maxNumber:
        minNumber, maxNumber = maxNumber, minNumber
    if minNumber <= x and maxNumber >= x:
        return True
    else:
        return False


def writeHeader(category,batch,grand_parent,permalink,title,description,stars,forks,watch,date,repo,page):
    s = """---
layout: project_page
title: """+title.title()+"""
permalink: """+permalink+"""
description: \""""+description+"""\"

has_children: false
parent: """+batch.upper()+ " " + grand_parent + """
grand_parent: """+grand_parent+"""

cover_url: https://cepdnaclk.github.io/projects.ce.pdn.ac.lk/data/categories/"""+category+"""/cover_page.jpg
thumbnail_url: https://cepdnaclk.github.io/projects.ce.pdn.ac.lk/data/categories/"""+category+"""/thumbnail.jpg

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
batch: e"""+batch+"""

default_thumb_image: https://cepdnaclk.github.io/projects.ce.pdn.ac.lk/data/categories/"""+tag+"""/thumbnail.jpg
description: """+description

    return template

def md_file_write(CATEGORIES,MIN,MAX):

    for i in CATEGORIES:
        index = open("docs/categories/"+str(i)+"/index.md",'r')
        index_data = index.read()


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
    # print(j)
    # print("\n\n\n\n")

    for p in range(1, 1000):

        r = requests.get(url=urlOrganizationRepos(p))
        jsonData = r.json()
        # print(urlOrganizationRepos(p))
        # sleep(60)

        # print(p, jsonData)
        # print("\n\n\n")

        if len(jsonData) == 0:
            break

        #removed if condition for checking year and batch in range
        for i in range(len(jsonData)):
            # print(jsonData[i]["name"])
            repoName = jsonData[i]["name"].strip().split("-")
            if repoName[0][0] == "e" and repoName[0][1:] != 'YY':
                #if repoName[1][1:] == "yp" and repoName[1][:1] != 'f':
                if repoName[1] in CATEGORIES:
                    print(repoName)
                    if(repoName[1][:1]=='c'):
                        year = int(repoName[1][2])
                    else:
                        year = int(repoName[1][:1])

                    batch = int(repoName[0][1:])


                    if(batch<MIN):
                        MIN = batch
                    if(batch>MAX):
                        MAX = batch

                    #if inRange(batch, START_BATCH, END_BATCH) and nRange(year, FIRST_YEAR, FINAL_YEAR):
                    filename = '-'.join(repoName[2:])

                        # TODO: update URLs
                        # /3yp/e15
                    path = "docs/github_repos/"+repoName[1]+"/" + repoName[0]+"/"+filename+".md"
                        #path = "docs/uncategorized/"+filename+".md"
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

                        # TODO: update other parameters on header
                        # writeHeader(category, batch, grand_parent, permalink, title,stars,forks,watch,date)
                    outputFile.write(writeHeader(repoName[1],repoName[0],grand_parent,permalink,capitalized,desc,stars,forks,watch,date,repo,page))
                    md_file_write(CATEGORIES,MIN,MAX)



print("END")
