from datetime import datetime
from datetime import timedelta
from time import mktime

import git

from blame import Blame

THRESHHOLD = 5
MONTHS_BACK = 3

"""
Potential options:

    - Months back
    - Percent threshhold
    - Specify repo directory

"""


def _older_than_x_months(commit, months_back):
    commit_date = datetime.fromtimestamp(mktime(commit.authored_date))
    return commit_date < datetime.today() - timedelta(days=months_back * 30)


def blame_meets_threshhold(blame, threshhold, months_back):
    for commit, lines_changed in blame:

        # ... for some reason gitpython blame gives a None commit at the end
        if not commit:
            continue

        if _older_than_x_months(commit, months_back) \
                and len(lines_changed) >= threshhold:
            print "Commit: '{}' ({}/{}), Change: {} ({}), exceeds threshholds."\
                .format(commit.id[:10], commit.authored_date.tm_mon,
                        commit.authored_date.tm_year, " ".join(
                            lines_changed)[:10], len(lines_changed))


def main():
    repo = git.Repo()
    latest_commit = repo.commits()[0]
    blobs = latest_commit.tree.values()
    for blob in blobs:
        blame = git.Blob.blame(repo, latest_commit, blob.name)
        blame = Blame(blame)
        print blame.filter()


if __name__ == '__main__':
    __package__ = 'docrot'
    main()
