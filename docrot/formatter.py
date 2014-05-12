from functools import partial
import os.path
import sys
import time

from clint.textui import colored, puts
import git

from blame import is_older_than, Blame


class FormatterBase(object):

    def __init__(self, directory, min_lines, months, stream=sys.stdout):
        """
        Coloring of dates will depend on how far the commit is after the
        age in months by multiples of 3.

        For instance, if ``5`` is passed, commits older than 5 months will be
        colored green, commits older than 10 months will be colored yellow,
        and commits older than 15 months will be colored red.
        """
        self.update_stream(stream)
        self.min_lines = min_lines
        self.months = months
        self.repo = git.Repo(directory)
        self.latest_commit = self.repo.commits()[0]
        self.blobs = self.latest_commit.tree.values()

    def _get_relative_age(self, commit):
        # Used for determining what visual style the commit should have.
        if is_older_than(commit, self.months * 3):
            return 'old'
        if is_older_than(commit, self.months * 2):
            return 'medium'
        else:
            return 'new'

    def update_stream(self, stream):
        """
        Created to allow on-the-fly injecting of new streams, such as when
        splitting output across multiple files.
        """
        self.p = partial(puts, newline=False, stream=stream.write)

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
        self.p("")

    def format(self):
        for blob in self.blobs:
            self.format_blob(blob)


class TextFormatter(FormatterBase):

    def _color_date(self, commit, text):
        age = self._get_relative_age(commit)
        ages_to_colors = {
            'old': colored.red,
            'medium': colored.yellow,
            'new': colored.green,
        }
        return str(ages_to_colors.get(age)(text))

    def format_blob(self, blob):
        self.p("/" + "-" * 78 + "\n")
        self.p("| {} \n".format(blob.name))
        super(TextFormatter, self).format_blob(blob)
        self.p("\\" + "-" * 78 + "\n\n")

    def format_line(self, commit, line, first=False):
        # Left column
        pre_first = "{}\t{}\t".format(
            commit.id[:10],
            time.strftime("%m/%d/%y", commit.authored_date))
        pre_first = self._color_date(commit, pre_first)
        pre_empty = "{}\t{}\t".format("." * 10, "." * 8)

        # Print the line
        self.p(pre_first if first else pre_empty)
        self.p(line)
        if "\n" not in line:
            self.p("\n")


class HtmlFormatter(FormatterBase):

    def format(self, *args, **kwargs):
        self.p("<style>{}</style>".format(self._get_css()))
        super(HtmlFormatter, self).format(*args, **kwargs)

    def _get_css(self):
        basepath = os.path.dirname(__file__)
        filepath = os.path.abspath(os.path.join(
            basepath, "assets", "style.css"))
        with open(filepath, 'rb') as f:
            return "".join(f.readlines())

    def format_blob(self, blob):
        self.p("<table>")
        self.p("<thead><td colspan=3>{}</td></thead>".format(blob.name))
        self.p("<tbody>")
        super(HtmlFormatter, self).format_blob(blob)
        self.p("</tbody>")
        self.p("</table>")

    def format_line(self, commit, line, first=False):
        self.p("<tr class='{} {}'>".format(
            self._get_relative_age(commit),
            "first" if first else "",  # allow for shading of the "..."
        ))
        if first:
            cols = (commit.id[:10],
                    time.strftime("%m/%d/%y", commit.authored_date))
        else:
            cols = ("." * 10, "." * 8)

        cols = cols + (line,)
        self.p("<td>{}</td><td>{}</td><td>{}</td>".format(*cols))

        self.p("</tr>")
