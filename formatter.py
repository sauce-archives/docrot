import time


class FormatterBase(object):

    def format_separator(self):
        return ""

    def format_commit(self, commit, lines_changed):
        return ""

    def format(self, buckets):
        # Discard empty buckets
        buckets = filter(lambda b: len(b) > 0, buckets)

        # Do the formatting
        output = ""
        for bucket in buckets:
            output += self.format_separator() + "\n"
            for commit, lines_changed in bucket:
                output += self.format_commit(commit, lines_changed) + "\n"
        return output


class TextFormatter(FormatterBase):

    def format_separator(self):
        return "-" * 79

    def format_commit(self, commit, lines_changed):
        output = ""

        # Left column
        pre_first = "{}\t{}\t".format(
            commit.id[:10],
            time.strftime("%m/%d/%y", commit.authored_date))
        pre_empty = "{}\t{}\t".format("." * 10, "." * 8)

        # Lines changed
        for i, line in enumerate(lines_changed):
            output += pre_first if i == 0 else pre_empty
            output += line + "\n"
        return output
