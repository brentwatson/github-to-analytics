# ActionableAgile github-to-analytics Script

Exports GitHub PR data to a CSV file that can be processed by ActionableAgile.com.

Similar to https://github.com/ActionableAgile/jira-to-analytics but exports GitHub PR data instead of Jira data.


# Usage

Update config section at top of `github-to-analytics.py` with your GH token 
([instructions](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token)),
repos, users, and date range to query for.


# Run

Run using:

```bash
python3.8 github-to-analytics.py
```

If there are import errors, run `pip install` and try again.
