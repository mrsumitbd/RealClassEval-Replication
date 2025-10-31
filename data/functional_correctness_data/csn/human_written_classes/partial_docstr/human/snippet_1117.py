import jinja2
import os
from pycparser.c_parser import CParser

class Library:
    """Symbols from a single DSO.

    Parameters
    ----------
    name : str
        Short name used to form symbol names.
    headers : Iterable[str]
        Header files to include.
    soname : str
        Name of library to load.
    guard : str
        Preprocessor expression governing conditional compilation.
    decls : str
        Prototypes of functions to be wrapped.
    wrappers : Iterable[str]
        Functions for which an implementation will be provided in the global
        namespace.
    optional : Iterable[str]
        Functions whose absence doesn't prevent the library being loaded. Calling
        such a function raises a std::system_error. The presence can be tested with
        another function, formed by prefixing the original function name with
        @c has_.
    """

    def __init__(self, name, headers, soname, guard, decls, wrappers=(), optional=(), *, fail_log_level='warning'):
        self.name = name
        self.headers = list(headers)
        self.soname = soname
        self.guard = guard
        ast = CParser().parse(decls)
        visitor = Visitor()
        visitor.visit(ast)
        self.nodes = visitor.nodes
        self.wrappers = list(wrappers)
        self.environment = jinja2.Environment(autoescape=False, trim_blocks=True, loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
        self.environment.filters['gen'] = gen_node
        self.environment.filters['gen_maybe_unused'] = gen_maybe_unused_node
        self.environment.filters['rename'] = rename_func
        self.environment.filters['ptr'] = make_func_ptr
        self.environment.filters['args'] = func_args
        self.environment.globals['name'] = self.name
        self.environment.globals['headers'] = self.headers
        self.environment.globals['soname'] = self.soname
        self.environment.globals['guard'] = self.guard
        self.environment.globals['nodes'] = self.nodes
        self.environment.globals['wrappers'] = set(wrappers)
        self.environment.globals['optional'] = set(optional)
        self.environment.globals['fail_log_level'] = fail_log_level

    def header(self):
        return self.environment.get_template('template.h').render()

    def cxx(self):
        return self.environment.get_template('template.cpp').render()