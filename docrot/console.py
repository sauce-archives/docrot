import argparse
import os

import git

from blame import Blame
from formatter import TextFormatter


def main():

    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", default=os.getcwd(),
                        help="directory containing repository to analyze")
    parser.add_argument("-t", "--threshhold", default=5,
                        help="number of consecutive lines in a row to trigger "
                             "alert")
    parser.add_argument("-m", "--months", default=5,
                        help="age in months required for commit line to be "
                             "determined to be old")
    args = parser.parse_args()

    # Process Repo
    repo = git.Repo(args.directory)
    latest_commit = repo.commits()[0]
    blobs = latest_commit.tree.values()
    for blob in blobs:
        blame = git.Blob.blame(repo, latest_commit, blob.name)
        blame = Blame(blame)
        buckets = blame.filter(min_lines=args.threshhold, months=args.months)
        TextFormatter(args.months).format(buckets)


if __name__ == '__main__':
    main()
