from functools import partial
import time

from clint.textui import puts, colored
import git

from blame import is_older_than, Blame


p = partial(puts, newline=False)


class FormatterBase(object):

    def __init__(self, directory, min_lines, months):
        self.min_lines = min_lines
        self.months = months
        self.repo = git.Repo(directory)
        self.latest_commit = self.repo.commits()[0]
        self.blobs = self.latest_commit.tree.values()

    def format_blob(self, blob):
        blame = git.Blob.blame(self.repo, self.latest_commit, blob.name)
        blame = Blame(blame)
        buckets = blame.filter(min_lines=self.min_lines,
                               months=self.months)
        # Discard empty buckets
        buckets = filter(lambda b: len(b) > 0, buckets)

        # Do the formatting
        for bucket in buckets:
            for commit, lines_changed in bucket:
                first = True
                for line in lines_changed:
                    self.format_line(commit, line, first=first)
                    first = False

    def format_line(self, commit, line, first=False):
        p("")

    def format(self):
        for blob in self.blobs:
            self.format_blob(blob)


class TextFormatter(FormatterBase):

    def __init__(self, directory, min_lines, months, color_months=None):
        """
        An optional ``color_months`` can be specified to color commits and
        dates depending on how far the commit is after the age in months by
        multipes of 3.

        For instance, if ``5`` is passed, commits older than 5 months will be
        colored green, commits older than 10 months will be colored yellow,
        and commits older than 15 months will be colored red.
        """
        super(TextFormatter, self).__init__(directory, min_lines, months)
        self._months = color_months

    def _color_date(self, commit, text):
        if not self._months:
            return text
        if is_older_than(commit, self._months * 3):
            return colored.red(text)
        if is_older_than(commit, self._months * 2):
            return colored.yellow(text)
        else:
            return colored.green(text)

    def format_blob(self, blob):
        p("/" + "-" * 78 + "\n")
        p("| {} \n".format(blob.name))
        super(TextFormatter, self).format_blob(blob)
        p("\\" + "-" * 78 + "\n\n")

    def format_line(self, commit, line, first=False):
        # Left column
        pre_first = "{}\t{}\t".format(
            commit.id[:10],
            time.strftime("%m/%d/%y", commit.authored_date))
        pre_first = self._color_date(commit, pre_first)
        pre_empty = "{}\t{}\t".format("." * 10, "." * 8)

        # Print the line
        p(pre_first if first else pre_empty)
        p(line)
        if "\n" not in line:
            p("\n")


class HtmlFormatter(FormatterBase):

    def format_blob(self, blob):
        p("<table>")
        super(HtmlFormatter, self).format_blob(blob)
        p("</table>")

    def format_line(self, commit, line, first=False):
        p("<tr>")
        if first:
            cols = (commit.id[:10],
                    time.strftime("%m/%d/%y", commit.authored_date))
        else:
            cols = ("." * 10, "." * 8)

        cols = cols + (line,)
        p("<td>{}</td><td>{}</td><td>{}</td>".format(*cols))

        p("</tr>")
