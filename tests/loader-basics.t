.. vim: ft=rst et sts=2 sw=2 tw=70

======================================================================
                      impala.Loader: basic tests
======================================================================

  >>> import os

Load the CUT: ::

  >>> from impala import Loader

Create a Loader pointing to a nonexistent location.
It will complain: ::

  >>> ldr0 = Loader(
  ...   'foo',
  ...   os.path.join(os.path.dirname(__file__), 'nonexistent')
  ... )
  Traceback (most recent call last):
    ...
  OSError: [Errno 2] No such file or directory: '...tests/nonexistent'

Create a Loader for a package: ::

  >>> ldr0 = Loader(
  ...   'foo',
  ...   os.path.join(os.path.dirname(__file__), 'fix0')
  ... )

Check that it has sensible `repr()` result: ::

  >>> repr(ldr0)
  "impala.Loader('foo', '...tests/fix0')"

Have it load something it is not responsible for: ::

  >>> bar = ldr0.load_module('bar')
  Traceback (most recent call last):
    ...
  AssertionError: Loader responsible for foo got request for bar

Have it load the correct package: ::

  >>> mod1 = ldr0.load_module('foo')
  >>> mod1
  <module 'foo' from '...tests/fix0/__init__.py'>

PEP302 lists some properties all modules must define: ::

  >>> mod1.__file__
  '...tests/fix0/__init__.py'
  >>> mod1.__name__
  'foo'
  >>> mod1.__package__
  'foo'
  >>> mod1.__path__
  ['...tests/fix0']
  >>> mod1.__loader__
  impala.Loader('foo', '...tests/fix0')
  >>> mod1.__loader__ is ldr0
  True

Verify that it actually loaded the code:

  >>> mod1.Something
  <class 'foo.Something'>

Create a Loader for a module: ::

  >>> ldr1 = Loader(
  ...   'foo',
  ...   os.path.join(os.path.dirname(__file__), 'fix1/guinea.py')
  ... )

Have it load something it is not responsible for: ::

  >>> bar = ldr1.load_module('bar')
  Traceback (most recent call last):
    ...
  AssertionError: Loader responsible for foo got request for bar

Have it load the correct package: ::

  >>> mod2 = ldr1.load_module('foo')
  >>> mod2
  <module 'foo' from '...tests/fix1/guinea.py'>

Verify that it actually loaded the code:

  >>> mod2.fun
  <function fun at 0x...>

