# REQUIREMENTS ------------
# pip install requests pytz
# -------------------------

import requests
import json
import os
from datetime import datetime
import pytz

tz_LK = pytz.timezone('Asia/Colombo')

notification_type = {
    "warning": {
        "color": 15258703,
        "icon": ":warning:"
    },
    "error": {
        "color": 16056320,
        "icon": ":smiling_imp:"
    },
    "debug": {
        "color": 8355711,
        "icon": ":lady_beetle:"
    },
    "info": {
        "color": 62830,
        "icon": ":information_source:"
    },
    "log": {
        "color": 62830,
        "icon": ":information_source:"
    }
}


class Notifications:

    def __init__(self, author, workflow, url="#"):
        self.author = author
        self.workflow = workflow
        self.url = url

        now = datetime.now(tz_LK)
        self.datetime = now.strftime("%Y/%m/%d %H:%M:%S")

    def get_webhook_url(self):
        return os.environ['webhook_url']

    def post_discord_message(self, data):
        headers = {
            'Content-Type': 'application/json'
        }
        # print(json.dumps(data, indent=4))
        response = requests.post(
            self.get_webhook_url(), headers=headers, data=json.dumps(data))
        if response.status_code == 204:
            print("Message sent successfully!")
        else:
            print("Error sending message. Response:")
            print(response.reason)

    def send(self, log_level, author, workflow, msg, description):
        level = log_level if log_level in notification_type else "info"
        data = {
            "username": "GitHub Actions",
            "author": {
                "name": self.author,
                "url": self.url,
                "icon_url": "https://cepdnaclk.github.io/assets/images/crest.png"
            },
            "embeds": [
                {
                    "title": "{0} `[{1}]` {2}.{3}".format(notification_type[level]["icon"], self.datetime, workflow, log_level.upper()),
                    "url": "",
                    "color": notification_type[level]["color"],
                    "fields":[
                        {
                            "name": "by `{0}`".format(author),
                            "value": msg,
                            "inline": False
                        }
                    ]
                }
            ]
        }

        if description != "":
            data['embeds'][0]['fields'].append({
                "name": "Description: ",
                "value": description,
                "inline": False
            })

        self.post_discord_message(data)

    def log(self, msg, description=''):
        self.send("log", self.author, self.workflow, msg, description)

    def warning(self, msg, description=''):
        self.send("warning", self.author, self.workflow, msg, description)

    def error(self, msg, description=''):
        self.send("error", self.author, self.workflow, msg, description)

    def debug(self, msg, description=''):
        self.send("debug", self.author, self.workflow, msg, description)

    def info(self, msg, description=''):
        self.send("info", self.author, self.workflow, msg, description)