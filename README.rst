.. vim: ft=rst sts=2 sw=2 tw=70
.. default-role:: literal

.. This file is marked up using reStructuredText.
   Lines beginning with ".." are reST directives.
   "foo_" or "`foo bar`_" is a link, defined at ".. _foo" or
   ".. _foo bar".
   "::" introduces a literal block (usually some form of code).
   "`foo`" is some kind of identifier.
   Suspicious backslashes in the text ("`std::string`\s") are required
   for reST to recognize the preceding character as syntax.

======================================================================
                              py-impala
======================================================================
----------------------------------------------------------------------
   Import packages and modules from arbitrary directories and files
----------------------------------------------------------------------

:Author: Roman Neuhauser
:Contact: neuhauser@sigpipe.cz
:Copyright: This document is in the public domain.


Overview
========

Impala is a PEP302_ protocol (`sys.meta_path` hook for the `import`
statement) implementation allowing the user to import packages and
modules from arbitrarily named directories and files.

.. _PEP302: http://www.python.org/dev/peps/pep-0302/


Motivation
==========

* Comfort and freedom in development
* Installed interface available without installation

Let's say I'm developing a Python package called `pyoneer`.  I want to
lay the source code out like this: ::

  README.txt
  src/
    __init__.py
    some.py
    more.py
  tests/
    ...

The question then is, how do I `import pyoneer` in the test files
(`<workdir>/tests/...`) and have it load `<workdir>/src/__init__.py`?
The default `import` mechanism requires packages to live in eponymous
directories.

What's the fuss about, you ask?  I should simply rename the `src`
directory to `pyoneer` or maybe `src/pyoneer`, no?

Indeed, this would be tolerable, at least with top-level packages.
However, if I'm working on something that will be available as
`foo.bar.baz` after installation, I certainly don't want to wade
through the desolate `src/foo/bar` to get to the source code.

Maybe I could `import src` in the tests instead?  Well, tests are
a form of documentation, and doubly so with `doctest`_.  "Proper"
documentation (README.txt, etc) can also contain snippets which
should be verifiable without the CUT being installed.

*Impala* to the rescue!

::

  import impala

  impala.register(dict(
    pyoneer = '<workdir>/src'
  ))

  import pyoneer

.. _doctest: http://docs.python.org/2/library/doctest.html


Description
===========

`impala.register(aliases)`
++++++++++++++++++++++++++

`aliases` is a `dict` mapping from fully-qualified module/package
names to paths to load from.  To load a package `p` from path
`/a/b/c`, `aliases` must include the key `p` with associated value
`/a/b/c`, and `/a/b/c/__init__.py` must be a valid package entry
point.  To load a module `m` from path `/k/l/m.py`, `aliases` must
include the key `m` with associated value `/k/l/m.py`.

Example: ::

  import impala

  impala.register({
    'p': '/a/b/c',
    'p.q': '/a/b/c/q',
    'p.q.m': '/a/b/c/q/m.py',
  })

  import p
  import p.q
  import p.q.m


License
=======

*py-impala* is distributed under the `MIT license`_.  See `LICENSE`_
for details.

.. _MIT license: http://...
.. _LICENSE: LICENSE


Installation
============

Using `pip` from PyPI_, the Python Package Index: ::

  pip install impala

From a checkout_ or extracted tarball: ::

  python setup.py install

.. _PyPI:     http://pypi.python.org/pypi
.. _checkout: https://github.com/roman-neuhauser/py-impala.git


Development
===========

Source code and issue tracker are at Github:

  https://github.com/roman-neuhauser/py-impala

