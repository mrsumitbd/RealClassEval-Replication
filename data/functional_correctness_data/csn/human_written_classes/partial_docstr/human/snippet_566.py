class ImportTracker:

    def __init__(self):
        self.cur_namespace_typing_imports = set()
        self.cur_namespace_adhoc_imports = set()

    def clear(self):
        self.cur_namespace_typing_imports.clear()
        self.cur_namespace_adhoc_imports.clear()

    def _register_typing_import(self, s):
        """
        Denotes that we need to import something specifically from the `typing` module.

        For example, _register_typing_import("Optional")
        """
        self.cur_namespace_typing_imports.add(s)

    def _register_adhoc_import(self, s):
        """
        Denotes an ad-hoc import.

        For example,
        _register_adhoc_import("import datetime")
        or
        _register_adhoc_import("from xyz import abc")
        """
        self.cur_namespace_adhoc_imports.add(s)