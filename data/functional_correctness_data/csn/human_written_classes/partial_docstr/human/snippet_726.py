import pybars._templates
import pybars

class FunctionContainer:
    """
    Used as a container for functions by the CodeBuidler
    """

    def __init__(self, name, code):
        self.name = name
        self.code = code

    @property
    def full_code(self):
        headers = u'import pybars\n\nif pybars.__version__ != %s:\n    raise pybars.PybarsError("This template was precompiled with pybars3 version %s, running version %%s" %% pybars.__version__)\n\nfrom pybars import strlist, Scope, PybarsError\nfrom pybars._compiler import _pybars_, escape, resolve, resolve_subexpr, prepare, ensure_scope\n\nfrom functools import partial\n\n\n' % (repr(pybars.__version__), pybars.__version__)
        return headers + self.code