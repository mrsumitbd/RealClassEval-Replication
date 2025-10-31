class Exporter:

    def __init__(self, globls):
        self._globals = globls

    def export(self, obj=None, *, name=None):
        if obj is None:
            def decorator(target):
                return self.export(target, name=name)
            return decorator

        export_name = name or getattr(obj, "__name__", None)
        if not export_name:
            raise ValueError(
                "Cannot determine export name. Provide a name=... or an object with __name__.")

        self._globals[export_name] = obj

        all_list = self._globals.get("__all__")
        if not isinstance(all_list, list):
            all_list = []
            self._globals["__all__"] = all_list
        if export_name not in all_list:
            all_list.append(export_name)

        return obj

    def __enter__(self):
        return self.export

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False
