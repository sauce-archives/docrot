import argparse
import os

from file_output import FileOutputWrapper
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
    parser.add_argument("-o", "--output", default=None,
                        help="(optional) split output into multiple files "
                             "in output directory, creating it if it"
                             "doesn't exist")

    args = parser.parse_args()

    # Process Repo
    if args.format == "text":
        formatter = TextFormatter(args.directory, args.threshhold,
                                  args.months)
        if args.output:
            formatter = FileOutputWrapper(formatter, 'txt', args.output)
        formatter.format()
    elif args.format == "html":
        formatter = HtmlFormatter(args.directory, args.threshhold,
                                  args.months)
        if args.output:
            formatter = FileOutputWrapper(formatter, 'html', args.output)
        formatter.format()


if __name__ == '__main__':
    main()
