from sacred.utils import convert_camel_case_to_snake_case

class CommandLineOption:
    """
    Base class for all command-line options.

    To implement a new command-line option just inherit from this class.
    Then add the `flag` class-attribute to specify the name and a class
    docstring with the description.
    If your command-line option should take an argument you must also provide
    its name via the `arg` class attribute and its description as
    `arg_description`.
    Finally you need to implement the `execute` classmethod. It receives the
    value of the argument (if applicable) and the current run. You can modify
    the run object in any way.

    If the command line option depends on one or more installed packages, those
    should be imported in the `apply` method to get a proper ImportError
    if the packages are not available.
    """
    _enabled = True
    short_flag = None
    ' The (one-letter) short form (defaults to first letter of flag) '
    arg = None
    ' Name of the argument (optional) '
    arg_description = None
    ' Description of the argument (optional) '

    @classmethod
    def get_flag(cls):
        flag = cls.__name__
        if flag.endswith('Option'):
            flag = flag[:-6]
        return '--' + convert_camel_case_to_snake_case(flag)

    @classmethod
    def get_short_flag(cls):
        if cls.short_flag is None:
            return '-' + cls.get_flag()[2]
        else:
            return '-' + cls.short_flag

    @classmethod
    def get_flags(cls):
        """
        Return the short and the long version of this option.

        The long flag (e.g. '--foo_bar'; used on the command-line like this:
        --foo_bar[=ARGS]) is derived from the class-name by stripping away any
        -Option suffix and converting the rest to snake_case.

        The short flag (e.g. '-f'; used on the command-line like this:
        -f [ARGS]) the short_flag class-member if that is set, or the first
        letter of the long flag otherwise.

        Returns
        -------
        (str, str)
            tuple of short-flag, and long-flag

        """
        return (cls.get_short_flag(), cls.get_flag())

    @classmethod
    def apply(cls, args, run):
        """
        Modify the current Run base on this command-line option.

        This function is executed after constructing the Run object, but
        before actually starting it.

        Parameters
        ----------
        args : bool | str
            If this command-line option accepts an argument this will be value
            of that argument if set or None.
            Otherwise it is either True or False.
        run :  sacred.run.Run
            The current run to be modified

        """
        pass