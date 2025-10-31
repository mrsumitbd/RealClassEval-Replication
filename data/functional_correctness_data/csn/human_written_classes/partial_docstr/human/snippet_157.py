class VCRFakeSocket:
    """
    A socket that doesn't do anything!
    Used when playing back cassettes, when there
    is no actual open socket.
    """

    def close(self):
        pass

    def settimeout(self, *args, **kwargs):
        pass

    def fileno(self):
        """
        This is kinda crappy.  requests will watch
        this descriptor and make sure it's not closed.
        Return file descriptor 0 since that's stdin.
        """
        return 0