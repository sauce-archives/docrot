from functools import partial
import time

from clint.textui import puts, colored

from blame import is_older_than


p = partial(puts, newline=False)


class FormatterBase(object):

    def format_separator(self):
        p("")

    def format_commit(self, commit, lines_changed):
        p("")

    def format(self, buckets):
        # Discard empty buckets
        buckets = filter(lambda b: len(b) > 0, buckets)

        # Do the formatting
        for bucket in buckets:
            self.format_separator()
            for commit, lines_changed in bucket:
                self.format_commit(commit, lines_changed)


class TextFormatter(FormatterBase):

    def __init__(self, color_months=None):
        """
        An optional ``color_months`` can be specified to color commits and
        dates depending on how far the commit is after the age in months by
        multipes of 3.

        For instance, if ``5`` is passed, commits older than 5 months will be
        colored green, commits older than 10 months will be colored yellow,
        and commits older than 15 months will be colored red.
        """
        self._months = color_months

    def format_separator(self):
        p(colored.magenta("\n" + "-" * 79 + "\n"))

    def _color_date(self, commit, text):
        if not self._months:
            return text
        if is_older_than(commit, self._months * 3):
            return colored.red(text)
        if is_older_than(commit, self._months * 2):
            return colored.yellow(text)
        else:
            return colored.green(text)

    def format_commit(self, commit, lines_changed):
        # Left column
        pre_first = "{}\t{}\t".format(
            commit.id[:10],
            time.strftime("%m/%d/%y", commit.authored_date))
        pre_first = self._color_date(commit, pre_first)
        pre_empty = "{}\t{}\t".format("." * 10, "." * 8)

        # Lines changed
        for i, line in enumerate(lines_changed):
            p(pre_first if i == 0 else pre_empty)
            p(line)
            if "\n" not in line:
                p("\n")
