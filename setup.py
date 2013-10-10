# vim: sw=2 sts=2 et fdm=indent

from distutils.core import setup
from glob import glob

def fread(path):
  with open(glob(path)[0]) as f:
    return f.read()

def version():
  return fread('VERSION').strip()

setup(
  name              = 'impala',
  version           = version(),
  author            = 'Roman Neuhauser',
  author_email      = 'neuhauser@sigpipe.cz',
  url               = 'https://github.com/roman-neuhauser/py-impala',
  description       = 'Import packages from "wrongly" named directories',
  long_description  = fread('README.*'),
  classifiers       = fread('pypi/classification').splitlines(),
  keywords          = 'PEP302 import',
  license           = 'MIT',
  packages          = ['impala'],
)

