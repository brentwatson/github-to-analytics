#!/usr/bin/env python3

import csv

from github import Github

from utils_github import check_and_wait_limit
from utils import calculate_cycle_time, calculate_working_hours, to_size_enum, to_cycle_time_enum

GITHUB_TOKEN = "YOUR_GH_TOKEN"
GITHUB_REPO = "org/repo"

OUTPUT_FILE = "output.csv"
MOST_RECENT_LIMIT = 100

'''
Output Most Recent GitHub PRs Cycle Time data to CSV file.
'''

github_client = Github(GITHUB_TOKEN)

with open(OUTPUT_FILE, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow([
        'ID',
        'Link',
        'Name',
        'Created At',
        'Reviewed At',
        'Approved At',
        'Merged At',
        'Closed At',
        'State',
        'Draft?',
        'Merged?',
        'Author',
        'N# Lines (Size)',
        'N# Commits',
        'N# Comments',
        'First Commenter',
        'First Approver',
        'Cycle Time (days)',
        'Cycle Time (working hours)',
        'Review Delay (working hours)',
        'Size Enum',
        'Cycle Time Enum',
        'Label-Automerge?',
        'Label-Documentation?',
        'Label-NDL?',
        'Label-Release?',
        'Label-RFC?',
    ])

    repo = github_client.get_repo(GITHUB_REPO)
    print("Gathering Data for: %s" % repo.name)

    pulls = repo.get_pulls(
        state='all',
        sort='created',
        direction='desc',
    )

    num_pulls = pulls.totalCount
    count = 0

    for pull in pulls[:MOST_RECENT_LIMIT]:
        # Check Github API limit
        check_and_wait_limit(github_client)

        count += 1
        print("Processing PR %d of %d: (%s) PR#%s" % (count, num_pulls, repo.name, pull.number))

        pr_size = pull.additions + pull.deletions
        pr_comments = list(pull.get_review_comments(since=pull.created_at))
        pr_approvals = list(filter(lambda x: x.state == "APPROVED", pull.get_reviews()))

        first_comment = pr_comments[0] if len(pr_comments) > 0 else None
        first_approval = pr_approvals[0] if len(pr_approvals) > 0 else None

        # Find First PR Review Activity
        first_review_activity = None
        if first_comment is not None:
            first_review_activity = first_comment.created_at
        elif first_approval is not None:
            first_review_activity = first_approval.submitted_at

        # Find Last PR Approval Activity
        last_approval_activity = pr_approvals[-1].submitted_at if len(pr_approvals) > 0 else None

        cycle_time = calculate_cycle_time(pull.created_at, pull.closed_at) if pull.closed_at else None
        working_hours_cycle_time = calculate_working_hours(pull.created_at, pull.closed_at) if pull.closed_at else None
        working_hours_review_delay = calculate_working_hours(pull.created_at, first_review_activity) if first_review_activity else None

        pr_labels = list(pull.get_labels())
        automerge = any(x.name == "Automerge" for x in pr_labels)
        documentation = any(x.name == "Documentation" for x in pr_labels)
        ndl = any(x.name == "NDL" for x in pr_labels)
        release = any(x.name == "Release" for x in pr_labels)
        rfc = any(x.name == "RFC" for x in pr_labels)

        csv_writer.writerow([
            pull.number,
            pull.html_url,
            pull.title,
            pull.created_at,  # PR Created
            first_review_activity if first_review_activity else None,  # PR Review In Progress
            last_approval_activity if last_approval_activity else None,  # PR Fully Approved
            pull.merged_at if pull.merged else None,  # PR Merged
            pull.closed_at,  # PR Closed
            pull.state,
            pull.draft,
            pull.merged,
            pull.user.login,
            pr_size,
            pull.commits,
            pull.review_comments + pull.comments,
            first_comment.user.login if first_comment else None,
            first_approval.user.login if first_approval else None,
            cycle_time,
            working_hours_cycle_time,
            working_hours_review_delay,
            to_size_enum(pr_size),
            to_cycle_time_enum(cycle_time) if cycle_time else None,
            automerge,
            documentation,
            ndl,
            release,
            rfc,
        ])

    csv_writer.writerow([])
