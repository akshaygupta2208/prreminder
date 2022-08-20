from datetime import datetime
import json
from github import Github
from urllib import request
import os


repo_string = os.environ['repo_string']
slack_endpoint = os.environ['slack_endpoint']
repo_list = repo_string.split(",")
github_token = os.environ['github_token']

g = Github(login_or_token=github_token, per_page=100)

pull_request_found = False
pr_data = {}

def send_message_to_slack(post):
    print("started executing send_message_to_slack")
    try:
        json_data = json.dumps(post)
        req = request.Request(slack_endpoint,
                              data=json_data.encode('ascii'),
                              headers={'Content-Type': 'application/json'})
        resp = request.urlopen(req)
        return True
    except Exception as em:
        print("EXCEPTION: " + str(em))
        return False


for repo in repo_list:
    r = g.get_repo(repo)
    now = datetime.now()
    for pull in r.get_pulls('open'):
        created_at = pull.created_at
        user = pull.user.login
        url = pull.html_url
        delta = (now.date() - created_at.date()).days
        if delta > 0:
            pull_request_found = True
            if user in pr_data:
                pr_list = pr_data[user]
                pr_list.append(url)
                pr_data[user] = pr_list
            else:
                pr_list = [url]
                pr_data[user] = pr_list
            print('found a pending pull request')
for user in pr_data:
    pr_list = pr_data[user]
    pr_text = ""
    for pr in pr_list:
        pr = pr.strip()
        pr_text = pr_text+pr + " \n\n"
    data = {
            "text": "*"+user+" your PRs are open for more than a day* - CRITICAL :hourglass:\n\n",
            "attachments": [{
                "color": "#f54242",
                "text": pr_text
            }
            ]
        }
    send_message_to_slack(data)
