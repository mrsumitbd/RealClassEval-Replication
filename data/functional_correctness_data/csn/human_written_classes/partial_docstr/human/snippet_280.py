from importlib.machinery import ModuleSpec as _ModuleSpec
import _jpype
import sys

class _JImportLoader:
    """ (internal) Finder hook for importlib. """

    def find_spec(self, name, path, target=None):
        if not _jpype.isStarted():
            base = name.partition('.')[0]
            if not base in _JDOMAINS:
                return None
            raise ImportError("Attempt to create Java package '%s' without jvm" % name)
        if name in _JDOMAINS:
            jname = _JDOMAINS[name]
            if not _jpype.isPackage(jname):
                raise ImportError("Java package '%s' not found, requested by alias '%s'" % (jname, name))
            ms = _ModuleSpec(name, self)
            ms._jname = jname
            return ms
        parts = name.rpartition('.')
        if not parts[1] and _jpype.isPackage(parts[2]):
            ms = _ModuleSpec(name, self)
            ms._jname = name
            return ms
        if not parts[1] and (not _jpype.isPackage(parts[0])):
            return None
        base = sys.modules.get(parts[0], None)
        if not base or not isinstance(base, _jpype._JPackage):
            return None
        name = unwrap(name)
        for customizer in _CUSTOMIZERS:
            if customizer.canCustomize(name):
                return customizer.getSpec(name)
        if not hasattr(base, parts[2]):
            try:
                cls = _jpype._java_lang_Class.forName(name, True, _jpype.JPypeClassLoader)
                if cls.getModifiers() & 1 == 0:
                    raise ImportError('Class `%s` is not public' % name)
                raise ImportError('Class `%s` was found but was not expected' % name)
            except Exception as ex:
                raise ImportError("Failed to import '%s'" % name) from ex
        return _ModuleSpec(name, self)
    ' (internal) Loader hook for importlib. '

    def create_module(self, spec):
        if spec.parent == '':
            return _jpype._JPackage(spec._jname)
        parts = spec.name.rsplit('.', 1)
        rc = getattr(sys.modules[spec.parent], parts[1])
        rc._handler = _JExceptionHandler
        return rc

    def exec_module(self, fullname):
        pass