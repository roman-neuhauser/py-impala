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

import os
import os.path as opa
import sys
import types

from . import fs

# this file includes snippets from PEP302 which reference
# the `imp` module, but this module is actually not used
# by the implementation, it's been deprecated in favor of
# importlib

def register(aliases):
  sys.meta_path.insert(0, Finder(aliases))

class Finder(object):
  def __init__(fdr, aliases):
    '''Create a mapping from `aliases.keys()` to `aliases.values()`.

       The `aliases` parameter is a `dict` with fully-qualified
       package or module names for keys and corresponding filesystem
       paths for values.

       With `<prefix>/here/__init__.py` and `<prefix>/there.py`, ::

         f = impala.Finder({
           'foo': '<prefix>/here',
           'bar': '<prefix>/there.py',
         })
         sys.meta_path.append(f)

         import foo
         import bar

       will load `./here/__init__.py` and `./there.py`.
    '''
    for alias, path in aliases.items():
      os.stat(path) # raises OSError if inaccessible
    fdr.aliases = aliases.copy()

  def __repr__(fdr):
    return '%s.%s(%s)' % (
      __name__,
      fdr.__class__.__name__,
      repr(fdr.aliases),
    )

  def find_module(fdr, fqname, path = None):
    '''Find a loader for module or package `fqname`.

       This method will be called with the fully qualified name
       of the module.  If the finder is installed on `sys.meta_path`,
       it will receive a second argument, which is `None` for
       a top-level module, or `package.__path__` for submodules
       or subpackages [5].
       It should return a loader object if the module was found, or
       `None` if it wasn't.  If `find_module()` raises an exception,
       it will be propagated to the caller, aborting the import.

       [5] The path argument to `finder.find_module()` is there
           because the `pkg.__path__` variable may be needed
           at this point.  It may either come from the actual
           parent module or be supplied by `imp.find_module()`
           or the proposed `imp.get_loader()` function.
    '''
    if fqname in fdr.aliases:
      return Loader(fqname, fdr.aliases[fqname])
    return None


class Loader(object):
  '''A loader object has one method: ::

       loader.load_module(fullname)

     This method returns the loaded module or raises an exception,
     preferably `ImportError` if an existing exception is not being
     propagated. If `load_module()` is asked to load a module that
     it cannot, `ImportError` is to be raised.

     The following set of methods may be implemented if support for
     (for example) Freeze-like tools is desirable. It consists of
     three additional methods which, to make it easier for the caller,
     each of which should be implemented, or none at all: ::

       loader.is_package(fullname)
       loader.get_code(fullname)
       loader.get_source(fullname)

     All three methods should raise `ImportError` if the module wasn't
     found.
  '''

  def __init__(ldr, scope, fspath):
    os.stat(fspath) # raises OSError if inaccessible
    ldr.scope = scope
    ldr.fspath = fspath

  def __repr__(ldr):
    return "%s.%s(%r, %r)" % (
      __name__,
      ldr.__class__.__name__,
      ldr.scope,
      ldr.fspath,
    )

  def load_module(ldr, fqname):
    '''Load `fqname` from under `ldr.fspath`.

       The `fqname` argument is the fully qualified module name,
       eg. "spam.eggs.ham".  As explained above, when ::

         finder.find_module("spam.eggs.ham")

       is called, "spam.eggs" has already been imported and added
       to `sys.modules`.  However, the `find_module()` method isn't
       necessarily always called during an actual import:
       meta tools that analyze import dependencies (such as freeze,
       Installer or py2exe) don't actually load modules, so
       a finder shouldn't depend on the parent package being
       available in `sys.modules`.

       The `load_module()` method has a few responsibilities that
       it must fulfill before it runs any code:

       * If there is an existing module object named 'fullname' in
         `sys.modules`, the loader must use that existing module.
         (Otherwise, the `reload()` builtin will not work correctly.)
         If a module named 'fullname' does not exist in
         `sys.modules`, the loader must create a new module object
         and add it to `sys.modules`.

         Note that the module object must be in `sys.modules`
         before the loader executes the module code. This is
         crucial because the module code may (directly or
         indirectly) import itself; adding it to `sys.modules`
         beforehand prevents unbounded recursion in the worst case
         and multiple loading in the best.

         If the load fails, the loader needs to remove any module it
         may have inserted into `sys.modules`. If the module was
         already in `sys.modules` then the loader should leave it
         alone.

       * The `__file__` attribute must be set. This must be a string,
         but it may be a dummy value, for example "<frozen>".
         The privilege of not having a `__file__` attribute at all
         is reserved for built-in modules.

       * The `__name__` attribute must be set. If one uses
         `imp.new_module()` then the attribute is set automatically.

       * If it's a package, the __path__ variable must be set.
         This must be a list, but may be empty if `__path__` has no
         further significance to the importer (more on this later).

       * The `__loader__` attribute must be set to the loader object.
         This is mostly for introspection and reloading, but can be
         used for importer-specific extras, for example getting data
         associated with an importer.

        The `__package__` attribute [8] must be set.

        If the module is a Python module (as opposed to a built-in
        module or a dynamically loaded extension), it should execute
        the module's code in the module's global name space
        (`module.__dict__`).

       [8] PEP 366: Main module explicit relative imports
           http://www.python.org/dev/peps/pep-0366/
    '''

    scope = ldr.scope.split('.')
    modpath = fqname.split('.')

    if scope != modpath[0:len(scope)]:
      raise AssertionError(
        "%s responsible for %s got request for %s" % (
          ldr.__class__.__name__,
          ldr.scope,
          fqname,
        )
      )

    if fqname in sys.modules:
      mod = sys.modules[fqname]
    else:
      mod = sys.modules.setdefault(fqname, types.ModuleType(fqname))

    mod.__loader__ = ldr

    fspath = ldr.path_to(fqname)

    mod.__file__ = str(fspath)

    if fs.is_package(fspath):
      mod.__path__ = [ldr.fspath]
      mod.__package__ = str(fqname)
    else:
      mod.__package__ = str(fqname.rpartition('.')[0])

    exec(fs.get_code(fspath), mod.__dict__)

    return mod

  def get_source(ldr, fqname):
    '''Get the source code for `fqname`.

    Should return the source code for the module as a string
    (using newline characters for line endings) or `None` if the
    source is not available (yet it should still raise
    `ImportError` if the module can't be found by the importer at
    all).
    '''
    return fs.get_source(ldr.path_to(fqname))

  def get_code(ldr, fqname):
    '''Get the code object for `fqname`.

       Should return the code object associated with the module,
       or `None` if it's a built-in or extension module.
       If the loader doesn't have the code object but it does have
       the source code, it should return the compiled source code.
       (This is so that our caller doesn't also need to check
       `get_source()` if all it needs is the code object.)
    '''
    return fs.get_code(ldr.path_to(fqname))

  def is_package(ldr, fqname):
    '''Indicate whether `fqname` designates a package (vs. module).

       Should return `True` if the module specified by `fqname`
       is a package and `False` if it isn't.
    '''
    return fs.is_package(ldr.path_to(fqname))

  def path_to(ldr, fqname):
    if fqname == ldr.scope:
      if opa.isfile(ldr.fspath):
        return ldr.fspath
      if opa.isdir(ldr.fspath):
        return opa.join(ldr.fspath, '__init__.py')

    raise ImportError('No module named %s' % fqname)

