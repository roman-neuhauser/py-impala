# vim: sw=2 sts=2 et

import sys
import os
import glob
import doctest
import unittest

testdir = os.path.dirname(__file__)

doctestflags = (
  doctest.DONT_ACCEPT_TRUE_FOR_1
| doctest.ELLIPSIS
| doctest.REPORT_ONLY_FIRST_FAILURE
)

def load_tests(loader, tests, pattern):
  '''`load_tests` Protocol implementation for `unittest` (new in 2.7)

  `doctest` seems to defer aggregate test runs to `unittest`
  '''
  tests.addTests(doctest.DocFileSuite(
    *find_tests(testdir),
    module_relative = False,
    optionflags = doctestflags
  ))
  return tests

def find_tests(testdir):
  return sorted(glob.glob(os.path.join(testdir, '*.t')))

if __name__ == '__main__':
  sys.path.insert(0, os.getcwd())
  unittest.main()
