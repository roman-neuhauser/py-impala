# vim: sw=2 sts=2 et fdm=indent

from __future__ import (
  absolute_import,
  division,
  generators,
  nested_scopes,
  print_function,
  unicode_literals,
  with_statement,
)

import os.path as opa

def get_source(fspath):
  with open(fspath) as fd:
    return fd.read()

def get_code(fspath):
  return compile(
    get_source(fspath),
    fspath,
    'exec',
    dont_inherit = True
  )

def is_package(fspath):
  return (
    opa.basename(fspath) == '__init__.py' and
    opa.exists(fspath)
  )

