from datetime import datetime
from datetime import timedelta
from itertools import izip_longest, islice
from time import mktime


class Peeker(object):

    def __init__(self, iterable):
        self._i = -1
        self._iter = iterable

    def __iter__(self):
        return self

    def _get(self, motion=1, peek=False):
        i = self._i + motion

        # The beginning or the end?
        if i + 1 == len(self._iter) or i < 0:
            if peek:
                return None
            else:
                raise StopIteration

        # Get the value
        _return = self._iter[i]
        if not peek:
            self._i += motion
        return _return

    def curr(self):
        return self._get(motion=0, peek=True)

    def next(self):
        return self._get(motion=1, peek=False)

    def prev(self):
        return self._get(motion=-1, peek=True)

    def peek(self):
        return self._get(motion=1, peek=True)


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

    def filter(self, min_lines=5, months=5):
        buckets = self._filter_by_age(self.blame, months)
        buckets = self._filter_by_lines(buckets, min_lines)
        return buckets
