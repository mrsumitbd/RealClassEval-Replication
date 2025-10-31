class Method:
    VALID_PLATFORM_NAMES = {'android', 'darwin', 'linux', 'windows', 'wsl', 'openbsd', 'freebsd', 'sunos', 'other'}
    platforms = set()
    method_type = ''
    network_request = False
    unusable = False

    def test(self):
        """Low-impact test that the method is feasible, e.g. command exists."""
        pass

    def get(self, arg):
        """
        Core logic of the method that performs the lookup.

        .. warning::
           If the method itself fails to function an exception will be raised!
           (for instance, if some command arguments are invalid, or there's an
           internal error with the command, or a bug in the code).

        Args:
            arg (str): What the method should get, such as an IP address
                or interface name. In the case of default_iface methods,
                this is not used and defaults to an empty string.

        Returns:
            Lowercase colon-separated MAC address, or None if one could
            not be found.
        """
        pass

    @classmethod
    def __str__(cls):
        return cls.__name__