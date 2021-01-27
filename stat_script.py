'''
    REQUIREMENTS:
        pip install requests
    AUTHORS:
        Gihan Jayatilake
        Akila Karunanayake
'''

import requests
import os
from datetime import datetime
import re, json
import base64


CATEGORIES={}
url = 'https://api.github.com/repos/cepdnaclk/projects/git/blobs/2166c8eba0801b62b539a23576a7b6fc46e7f4f7'
resp = requests.get(url)
#print(resp)
data = json.loads(resp.text)
#print(data)
#print(data['content'])

message_bytes = base64.b64decode(data['content'])
message = json.loads(message_bytes.decode('ascii'))

for i in message:
    CATEGORIES[message[i]['link']] = message[i]['name']
    #print(message[i]['link'])
print(CATEGORIES)

ORGANIZATION = "cepdnaclk"
PROJECTS = []
START_BATCH = 10
END_BATCH = 16
FIRST_YEAR = 2
FINAL_YEAR = 4


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


def writeHeader(category, batch, grand_parent, permalink, title,stars,forks,watch,date):
    s = """---
layout: project_page
title: """+title+"""
permalink: """+permalink+"""
description: ""

has_children: false
parent: """+batch+ " " + grand_parent + """
grand_parent: """+grand_parent+"""

cover_url: https://cepdnaclk.github.io/projects/data/categories/"""+category+"""/cover_page.jpg
thumbnail_url: https://cepdnaclk.github.io/projects/data/categories/"""+category+"""/thumbnail.jpg

repo_url: #
page_url: #

forks: """+str(forks)+"""
watchers: """+str(watch)+"""
stars: """+str(stars)+"""
started_on: """+date+"""

---
    """
    return s


if __name__ == "__main__":
    print("START")
    URL = urlOrganization()

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

        for i in range(len(jsonData)):
            # print(i)
            repoName = jsonData[i]["name"].strip().split("-")
            if repoName[0][0] == "e" and repoName[0][1:] != 'YY':
                if repoName[1][1:] == "yp" and repoName[1][:1] != 'f':
                    batch = int(repoName[0][1:])
                    year = int(repoName[1][:1])
                    if inRange(batch, START_BATCH, END_BATCH) and inRange(year, FIRST_YEAR, FINAL_YEAR):
                        filename = '-'.join(repoName[2:])

                        # TODO: update URLs
                        path = "docs/uncategorized/"+filename+".md"
                        title = ' '.join(repoName[2:])
                        permalink = "/"+repoName[1]+"/" + repoName[0]+"/"+filename
                        stars = jsonData[i]["stargazers_count"]
                        forks = jsonData[i]["forks_count"]
                        watch = jsonData[i]["watchers_count"]
                        date = jsonData[i]["created_at"]

                        outputFile = open(path, "w+")
                    

                        # TODO: update other parameters on header
                        outputFile.write(writeHeader(repoName[1],repoName[0][1:], "Unified", permalink, title,stars,forks,watch,date))
print("END")
