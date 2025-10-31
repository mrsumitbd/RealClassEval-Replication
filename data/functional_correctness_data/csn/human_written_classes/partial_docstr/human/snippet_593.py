import sys

class NotAModule:
    """
    A class to implement an informative error message that will be outputted if
    someone tries to use an on-demand import without having the requisite
    package installed.
    """

    def __init__(self, pkg_name, exc=None):
        self.pkg_name = pkg_name
        self._original_exception = exc
        error_note = f'Something went wrong while trying to lazy-import {pkg_name}. Please make sure that {pkg_name} is properly installed.\nIf the problem persists, please file an issue at https://github.com/yt-project/unyt/issues/new'
        if exc is None:
            self.error = ImportError(error_note)
        elif sys.version_info >= (3, 11):
            exc.add_note(error_note)
            self.error = exc
        else:
            self.error = type(exc)(f'{exc!s}\n{error_note}').with_traceback(exc.__traceback__)

    def __getattr__(self, item):
        raise self.error

    def __call__(self, *args, **kwargs):
        raise self.error

    def __repr__(self) -> str:
        if self._original_exception is None:
            return f'NotAModule({self.pkg_name!r})'
        else:
            return f'NotAModule({self.pkg_name!r}, {self._original_exception!r})'