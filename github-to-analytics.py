#!/usr/bin/env python3

from datetime import datetime, timedelta
from github import Github
import csv

GITHUB_TOKEN = "YOUR_GH_TOKEN"
DAYS = 90
REPOS = ["org1/repo1", "org1/repo2"]
USERS = ["user1", "user2"]

'''
Output GitHub PR data as CSV file.
'''
query_start_time = datetime.today() - timedelta(days=DAYS)
g = Github(GITHUB_TOKEN)
with open('output.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['ID', 'Link', 'Name', 'Backlog', 'In Progress', 'Done', 'State', 'User'])

    for gh_repo in REPOS:
        repo = g.get_repo(gh_repo)
        for user in USERS:
            print("Gathering Data for: %s - %s" % (repo.name, user))
            pulls = repo.get_issues(
                state='all',
                direction='asc',
                since=query_start_time,
                creator=user
            )

            num_pulls = pulls.totalCount
            count = 0

            for pull in pulls:
                count += 1
                print("Processing PR %d of %d: (%s) PR#%s" % (count, num_pulls, repo.name, pull.number))
                csv_writer.writerow([
                    pull.number,
                    pull.url,
                    pull.title,
                    pull.created_at.date(),  # Backlog (doesn't really apply to PRs)
                    pull.created_at.date(),  # In Progress
                    pull.closed_at.date() if pull.closed_at else None,  # Done (Also pull.merged_at)
                    pull.state,
                    pull.user.login,
                ])

    csv_writer.writerow([])
