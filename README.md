# GitHubFlames
A Python script that calculates a GitHub Streak

## What is a Streak
The script uses the GitHub Api to search for recent user activity. 
If the user is continually contributing the days are counted, this is called a GitHub Streak.
If you stop for 24 hours your start again.

Currently, only commits are counted as activity.

## Installation
1. Clone the repo.
2. Enter the API Token or Login to `login.yaml`. See `example.login.yaml` as example.
3. Run the `main.py` file, which returns the Streak as an integer.