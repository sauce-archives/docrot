docrot
------

Description
~~~~~~~~~~~

docrot is intended to find continuous segments of documentation in a
repository that have not been updated in a long time.  In theory this could be
used against non-documentation related codebases, but at the moment the
formatting is only being tested against github's wiki format.

Installation
~~~~~~~~~~~~

Clone the repo, then::

	``pip install .``

Usage
~~~~~

Just ``cd`` to your documentation repo and run::

	``docrot``

By default, areas of documentation that are 5 months old and at least 5 lines
long will be shown.  For additional options and customization::

	``docrot -h``
