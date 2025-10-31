class _Options:
    """Base class for classes holding command-line arguments.

    The derived class must have attributes corresponding to the command-line
    arguments (with the same name).

    Parameters
    ----------
    name_map : Optional[Mapping[str, Optional[str]]]
        If specified, provides for renaming and suppressing command-line
        options. If ``name_map['foo_bar'] == 'abc_xyz'`` then the end user will
        pass ``--abc-xyz`` instead of ``--foo-bar``. Setting an element to
        ``None`` will suppress the option.
    """

    def __init__(self, name_map=None):
        self._name_map = name_map or {}

    def _add_argument(self, parser, name, *args, **kwargs):
        """Add an argument to a parser.

        This is called by subclasses to add an argument to a parser.

        It functions like :py:meth:`argparse.ArgumentParser.add_argument`, except
        that:

        - Instead of the flag, one must provide the name of the class
          attribute. The flag is computed by converting underscores to dashes and
          prepending ``--`` (after applying the name map given to the
          constructor).
        - No `default` should be provided. The value currently stored in the object
          is used as the default.
        """
        assert 'dest' not in kwargs
        new_name = self._name_map.get(name, name)
        if new_name is not None:
            flag = '--' + new_name.replace('_', '-')
            parser.add_argument(flag, *args, dest=new_name, default=getattr(self, name), **kwargs)

    def _extract_args(self, namespace):
        """Update the object attributes from parsed arguments.

        After parsing the arguments, the subclass should call this to reflect
        the arguments into the object.
        """
        for name in self.__dict__:
            if name.startswith('_'):
                continue
            mapped_name = self._name_map.get(name, name)
            if mapped_name is not None:
                setattr(self, name, getattr(namespace, mapped_name))