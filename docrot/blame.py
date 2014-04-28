from datetime import datetime
from datetime import timedelta
from itertools import izip_longest, islice
from time import mktime


class Blame(object):

    def __init__(self, blame):
        self._blame = blame

    @property
    def blame(self):
        # ... for some reason gitpython blame gives a None commit at the end
        return filter(lambda x: x[0] is not None, self._blame)

    def _is_older_than(self, commit, months):
        commit_date = datetime.fromtimestamp(mktime(commit.authored_date))
        return commit_date < datetime.today() - timedelta(days=months * 30)

    def _filter_by_age(self, blame, months):
        """
        Groups the lines of a blame into continuous buckets that fit the age
        thresshold.
        """
        buckets = []

        bucket = []
        for commit, lines_changed in blame:
            if self._is_older_than(commit, months):
                bucket.append((commit, lines_changed))
            elif bucket:
                buckets.append(bucket)
                bucket = []

        return buckets

    def _filter_by_lines(self, buckets, min_lines):
        lines_in_bucket = lambda b: islice(izip_longest(*b), 1).next()
        bucket_big_enough = lambda b: len(lines_in_bucket(b)) > min_lines
        return filter(bucket_big_enough, buckets)

    def filter(self, min_lines, months):
        """
        Filters a gitpython blame result to include consecutive lines larger
        than ``min_lines`` and older than ``months``.
        """
        buckets = self._filter_by_age(self.blame, months)
        return self._filter_by_lines(buckets, min_lines)
