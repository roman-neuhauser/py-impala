.. vim: ft=rst et sts=2 sw=2 tw=70

======================================================================
                      impala.Finder: basic tests
======================================================================

Load the CUT: ::

  >>> from impala import Finder

Create a Finder pointing to a nonexistent location.
It will complain: ::

  >>> import os.path
  >>> fdr0 = Finder(dict(
  ...   foo = os.path.join(os.path.dirname(__file__), 'nonexistent')
  ... ))
  Traceback (most recent call last):
    ...
  OSError: [Errno 2] No such file or directory: '...tests/nonexistent'

Create a Finder pointing to an existing directory. ::

  >>> fdr0 = Finder(dict(
  ...   foo = os.path.join(os.path.dirname(__file__), 'fix0')
  ... ))

Check that it has sensible `repr()` result: ::

  >>> repr(fdr0)
  "impala.Finder({'foo': '...tests/fix0'})"

Ask the finder for a loader for a package it governs:

  >>> ldr0 = fdr0.find_module('foo', None)
  >>> repr(ldr0)
  "impala.Loader('foo', '...tests/fix0')"

Create a Finder pointing to an existing file. ::

  >>> fdr1 = Finder(dict(
  ...   bar = os.path.join(os.path.dirname(__file__), 'fix1/guinea.py')
  ... ))

Ask the finder for a loader for a module it governs:

  >>> ldr1 = fdr1.find_module('bar', None)
  >>> repr(ldr1)
  "impala.Loader('bar', '...tests/fix1/guinea.py')"

