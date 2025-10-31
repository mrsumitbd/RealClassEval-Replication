import os
import pickle
import hashlib
from pyuploadcare.ucare_cli.commands.helpers import bar, bool_or_none, int_or_none, pprint, promt

class SyncSession:
    """Provides an ability to save current state of iteration if any errors
    happened during iteration. After that is possible to restore this state
    and continue from that point.
    """

    def __init__(self, file_list, no_input=False):
        parts = str(file_list.__dict__)
        self.session = file_list
        self.no_input = no_input
        self.signature = hashlib.md5(parts.encode('utf-8')).hexdigest()
        self.session_filepath = os.path.join(os.path.expanduser('~'), '.{0}.sync'.format(self.signature))
        if os.path.exists(self.session_filepath):
            if not self.no_input and promt('Continue last sync?'):
                with open(self.session_filepath, 'rb') as f:
                    client = self.session._client
                    self.session = pickle.load(f)
                    self.session._client = client
                    return

    def __enter__(self):
        return self.session

    def __exit__(self, *args):
        if all(args):
            with open(self.session_filepath, 'wb') as f:
                client = self.session._client
                self.session._client = None
                pickle.dump(self.session, f)
                self.session._client = client
            return False
        if os.path.exists(self.session_filepath):
            try:
                os.remove(self.session_filepath)
            except OSError:
                pass
        return True