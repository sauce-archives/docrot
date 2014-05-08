import argparse
import os

from formatter import TextFormatter, HtmlFormatter


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
    parser.add_argument("-f", "--format", default="text",
                        help="format of output")
    args = parser.parse_args()

    # Process Repo
    if args.format == "text":
        TextFormatter(args.directory, args.threshhold, args.months).format()
    elif args.format == "html":
        HtmlFormatter(args.directory, args.threshhold, args.months).format()


if __name__ == '__main__':
    main()
