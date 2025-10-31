from tempfile import mkdtemp, template
import shutil

class TemporaryDirectory:
    """Create and return a temporary directory.

    This has the same behavior as mkdtemp but can be used as a context manager.

    Upon exiting the context, the directory and everything contained
    in it are removed.

    Examples
    --------
    >>> import os
    >>> with TemporaryDirectory() as tmpdir:
    ...     fname = os.path.join(tmpdir, 'example_file.txt')
    ...     with open(fname, 'wt') as fobj:
    ...         _ = fobj.write('a string\\n')
    >>> os.path.exists(tmpdir)
    False
    """

    def __init__(self, suffix='', prefix=template, dir=None):
        self.name = mkdtemp(suffix, prefix, dir)
        self._closed = False

    def __enter__(self):
        """Return the directory managed by this context."""
        return self.name

    def cleanup(self):
        """Delete the directory managed by this context if it exists."""
        if not self._closed:
            shutil.rmtree(self.name)
            self._closed = True

    def __exit__(self, exc, value, tb):
        """Clean up the directory on exit."""
        self.cleanup()
        return False