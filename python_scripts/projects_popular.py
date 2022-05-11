import requests
import os
import json
from operator import itemgetter
import random

url = '../_data/projects.json'
with open(url, 'r') as f:
    projects = json.load(f)

filtered_list = []

# Intermediate list
for p in projects:
    updated = projects[p]['updated_at']
    projects[p]['name'] = p
    stars = projects[p]['stars_count']
    watchers = projects[p]['watchers_count']
    forks = projects[p]['forks_count']

    # Calculate the score based on weights, and round to 3 digits
    score = round(stars*0.5 + watchers*0.3 + forks*0.2, 3)
    projects[p]['popularity_score'] = float(score)
    
    projects[p]['project_url'] = projects[p]['project_url'].replace("https://projects.ce.pdn.ac.lk", "")

    # Only consider the projects with positive scores
    if(score>0):
        filtered_list.append(projects[p])

# Sort as the highest scored projects first
sorted_list = sorted(filtered_list, key=itemgetter('popularity_score'), reverse=True)

# Only latest x projects will be saved here
TOP_PROJ_LIMIT = 8
sliced_list = sorted_list[:TOP_PROJ_LIMIT]

# Suffel the projects
random.shuffle(sliced_list)

# Prepare a dictionary with the project name as the key
result = { sliced_list[i]['name'] : sliced_list[i] for i in range(0, len(sliced_list) ) }

# Write project data into file
filename = "../_data/projects_popular.json"
os.makedirs(os.path.dirname(filename), exist_ok=True)
with open(filename, "w") as f:
    f.write(json.dumps(result, indent = 4))
