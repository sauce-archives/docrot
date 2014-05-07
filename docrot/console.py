import argparse
import os

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
    TextFormatter(args.directory, args.threshhold, args.months, 5).format()


if __name__ == '__main__':
    main()
