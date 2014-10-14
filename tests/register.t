.. vim: ft=rst et sts=2 sw=2 tw=70

======================================================================
                        impala.register tests
======================================================================

Load the CUT::

  >>> import impala

Basic operation (success)::

  >>> impala.register(dict(rofl = 'tests/fix0'))
  >>> import rofl
  >>> rofl.__file__
  'tests/fix0/__init__.py'

Basic operation (failure)::

  >>> try:
  ...   impala.register(dict(rofl = 'tests/nonexistent'))
  ... except OSError as e:
  ...   print(e)
  [Errno 2] No such file or directory: 'tests/nonexistent'

