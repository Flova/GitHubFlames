import os
import yaml
import datetime
from github import Github


class GitHubFlames(object):
    """
    Calculate a GitHub streak
    """
    def __init__(self):
        # Create path
        project_path = os.path.abspath(os.path.dirname(__file__))

        # Load login data
        with open(os.path.join(project_path, "login.yaml"), "r") as f:
            login_data = yaml.safe_load(f)

        # Generate GitHub object placeholder
        gh = None

        # Parse login data
        try:
            if login_data['token'] is not None:
                if isinstance(login_data['token'], str):
                    # Login user with token
                    gh = Github(login_data['token'])
                else:
                    raise TypeError

            if login_data['username'] is not None \
                    and login_data['password'] is not None:
                if isinstance(login_data['username'], str) and isinstance(login_data['password'], str):
                    # Login user with username and password
                    gh = Github(login_data['username'], login_data['password'])
                else:
                    raise TypeError
        except KeyError:
            print("Please set correct .login.yaml file!")
            return False

        if gh is None:
            print("Please set an login in the .login.yaml!")
            return False

        # Get user
        self.me = gh.get_user()

    def commit_in_range(self, user, start_time, end_time):
        """
        Returns if the user is author of a commit in one of it's repositories.

        :param user: A github user
        :param start_time: datetime
        :param end_time: datetime
        :return: bool
        """

        for repo in user.get_repos():
            # Check if repo is edited today
            if start_time < repo.pushed_at:
                for commit in repo.get_commits():
                    # Get commit time
                    commit_date = commit.commit.author.date
                    if commit_date < start_time:
                        break
                    if commit.author.id == user.id and commit_date < end_time:
                        return True
        return False

    def commited_days_ago(self, user, days):
        """
        Checks if the user commited n days ago. A day is represented as -24h

        :param user: A github user
        :param days: Number of days in the past
        :return: bool
        """

        now = datetime.datetime.utcnow()
        now = now.replace(hour=23, minute=59, second=59, microsecond=999)
        end = now - datetime.timedelta(days=days)
        begin = now - datetime.timedelta(days=days+1)
        return self.commit_in_range(user, begin, end)

    def streak(self, user=None, offset=0):
        """
        Calculates the gitHub Streak counted in days.

        :param user: A github user
        :param offset: Date offset, default is 1 to show only the streak until yesterday,
        otherwise the streak changes from 0 to 'streak' count if you commit.
        :return: Streak days
        """
        if user is None:
            user = self.me
        days = -1
        days += offset
        streak_active = True

        while streak_active:
            days += 1
            streak_active = self.commited_days_ago(user, days)

        days -= offset
        return days


if __name__ == "__main__":
    ghf = GitHubFlames()
    streak_length = ghf.streak()
    print(streak_length)
