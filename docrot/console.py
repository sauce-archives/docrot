import git

from blame import Blame
from formatter import TextFormatter

THRESHHOLD = 5
MONTHS_BACK = 3

"""
Potential options:

    - Months back
    - Percent threshhold
    - Specify repo directory

"""


def main():
    repo = git.Repo()
    latest_commit = repo.commits()[0]
    blobs = latest_commit.tree.values()
    for blob in blobs:
        blame = git.Blob.blame(repo, latest_commit, blob.name)
        blame = Blame(blame)
        buckets = blame.filter()
        print TextFormatter().format(buckets)


if __name__ == '__main__':
    main()
