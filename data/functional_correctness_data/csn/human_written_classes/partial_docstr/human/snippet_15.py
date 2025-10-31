import re

class GhostscriptFollower:
    """Parses the output of Ghostscript and uses it to update the progress bar."""
    re_process = re.compile('Processing pages \\d+ through (\\d+).')
    re_page = re.compile('Page (\\d+)')

    def __init__(self, progressbar_class):
        self.count = 0
        self.progressbar_class = progressbar_class
        self.progressbar = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.progressbar:
            return self.progressbar.__exit__(exc_type, exc_value, traceback)
        return False

    def __call__(self, line):
        if not self.progressbar_class:
            return
        if not self.progressbar:
            m = self.re_process.match(line.strip())
            if m:
                self.count = int(m.group(1))
                self.progressbar = self.progressbar_class(total=self.count, desc='PDF/A conversion', unit='page')
                self.progressbar.__enter__()
        elif self.re_page.match(line.strip()):
            self.progressbar.update()