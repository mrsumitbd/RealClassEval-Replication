import os

class BaseCompressor:
    suffix = None

    def __init__(self, settings):
        self.suffixes_to_compress = settings.get('suffixes', DEFAULT_SETTINGS['suffixes'])

    def do_compress(self, filename, compressed_filename):
        """
        Perform actual compression.
        This should be implemented by subclasses.
        """
        raise NotImplementedError

    def compress(self, filename):
        """Compress a file, only if needed."""
        compressed_filename = self.get_compressed_filename(filename)
        if not compressed_filename:
            return
        self.do_compress(filename, compressed_filename)

    def get_compressed_filename(self, filename):
        """If the given filename should be compressed, returns the
        compressed filename.

        A file can be compressed if:

        - It is a whitelisted extension
        - The compressed file does not exist
        - The compressed file exists by is older than the file itself

        Otherwise, it returns False.

        """
        if os.path.splitext(filename)[1][1:] not in self.suffixes_to_compress:
            return False
        file_stats = None
        compressed_stats = None
        compressed_filename = f'{filename}.{self.suffix}'
        try:
            file_stats = os.stat(filename)
            compressed_stats = os.stat(compressed_filename)
        except OSError:
            pass
        if file_stats and compressed_stats:
            return compressed_filename if file_stats.st_mtime > compressed_stats.st_mtime else False
        else:
            return compressed_filename