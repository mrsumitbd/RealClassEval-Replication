from hidet.option import set_option as _set_hidet_option

class debug:

    @staticmethod
    def dump_ir(enable: bool=True) -> None:
        """
        Whether to dump the IR during compilation.

        Parameters
        ----------
        enable: bool
            The flag to enable or disable dumping the IR. Default is True.
        """
        return _set_hidet_option('tilus.debug.dump_ir', enable)

    @staticmethod
    def launch_blocking(enabled: bool=True) -> None:
        """
        Whether to block the launch of the kernel until the kernel is finished.

        Parameters
        ----------
        enabled: bool
            The flag to enable or disable blocking the launch of the kernel. Default is True.
        """
        return _set_hidet_option('tilus.debug.launch_blocking', enabled)