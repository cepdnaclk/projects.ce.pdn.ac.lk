import requests
import os
import json

url = '../_data/projects.json'
with open(url, 'r') as f:
    projects = json.load(f)


# Get latest 10 projects
# Sort Dictionary by value in descending order using lambda function

updated_dict = {}
sorted_dict = {}

# Intermediate dict
for p in projects:
    updated = projects[p]['updated_at']
    projects[p]['name'] = p
    updated_dict[updated] = projects[p]
    updated_dict[updated]['project_url'] = updated_dict[updated]['project_url'].replace("https://projects.ce.pdn.ac.lk", "")

# Final dict
for key in sorted(updated_dict, reverse=True):
    sorted_dict[updated_dict[key]['name']] = updated_dict[key]


# Only latest x projects will be saved here
LATEST_PROJ_LIMIT = 8
sliced_dict = dict(list(sorted_dict.items())[:LATEST_PROJ_LIMIT])

# Write project data into file
filename = "../_data/projects_latest.json"
os.makedirs(os.path.dirname(filename), exist_ok=True)
with open(filename, "w") as f:
    f.write(json.dumps(sliced_dict, indent = 4))
