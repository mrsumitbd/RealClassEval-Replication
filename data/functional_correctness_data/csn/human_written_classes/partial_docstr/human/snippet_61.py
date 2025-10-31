import base64
import hashlib
import os

class _Record:
    """
    Internal - builds up text suitable for writing to a RECORD item, e.g.
    within a wheel.
    """

    def __init__(self):
        self.text = ''

    def add_content(self, content, to_, verbose=True):
        if isinstance(content, str):
            content = content.encode('utf8')
        h = hashlib.sha256(content)
        digest = h.digest()
        digest = base64.urlsafe_b64encode(digest)
        digest = digest.rstrip(b'=')
        digest = digest.decode('utf8')
        self.text += f'{to_},sha256={digest},{len(content)}\n'
        if verbose:
            log2(f'Adding {to_}')

    def add_file(self, from_, to_):
        log1(f'Adding file: {os.path.relpath(from_)} => {to_}')
        with open(from_, 'rb') as f:
            content = f.read()
        self.add_content(content, to_, verbose=False)

    def get(self, record_path=None):
        """
        Returns contents of the RECORD file. If `record_path` is
        specified we append a final line `<record_path>,,`; this can be
        used to include the RECORD file itself in the contents, with
        empty hash and size fields.
        """
        ret = self.text
        if record_path:
            ret += f'{record_path},,\n'
        return ret