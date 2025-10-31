from sacred.utils import join_paths, SacredError

class ReadOnlyContainer:

    def __reduce__(self):
        return (self.__class__, (self.__copy__(),))

    def _readonly(self, *args, **kwargs):
        raise SacredError('The configuration is read-only in a captured function!', filter_traceback='always')