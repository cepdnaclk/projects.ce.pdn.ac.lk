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


def writeHeader(category, batch, grand_parent, permalink, title):
    s = """---
layout: project_page
title: """+title+"""
permalink: """+permalink+"""
description: ""

has_children: false
parent: """+batch+ " " + grand_parent + """
grand_parent: """+grand_parent+"""

cover_url: https://cepdnaclk.github.io/projects.ce.pdn.ac.lk/data/categories/3yp/data/categories/"""+category+"""/cover_page.jpg
thumbnail_url: https://cepdnaclk.github.io/projects.ce.pdn.ac.lk/data/categories/3yp/data/categories/"""+category+"""/thumbnail.jpg

repo_url: #
page_url: #

forks: 0
watchers: 0
stars: 0
started_on: yyyy-mm-dd

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
                        outputFile = open(path, "w+")

                        # TODO: update other parameters on header
                        outputFile.write(writeHeader(repoName[1],repoName[0][1:], "Unified", permalink, title))
print("END")
