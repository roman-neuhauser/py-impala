.. vim: ft=rst et sts=2 sw=2 tw=70

======================================================================
                        impala.register tests
======================================================================

Load the CUT: ::

  >>> import impala

Basic operation (success): ::

  >>> impala.register(dict(rofl = 'tests/fix0'))
  >>> import rofl
  >>> rofl
  <module 'rofl' from '...tests/fix0/__init__.py'>

Basic operation (failure): ::

  >>> impala.register(dict(rofl = 'tests/nonexistent'))
  Traceback (most recent call last):
    ...
  OSError: [Errno 2] No such file or directory: '...tests/nonexistent'

