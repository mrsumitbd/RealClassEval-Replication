import sys

class _exec_once:
    """Deal with memory_usage calling functions more than once (argh)."""

    def __init__(self, code, fake_main):
        self.code = code
        self.fake_main = fake_main
        self.run = False

    def __call__(self):
        if not self.run:
            self.run = True
            old_main = sys.modules.get('__main__', None)
            with patch_warnings():
                sys.modules['__main__'] = self.fake_main
                try:
                    exec(self.code, self.fake_main.__dict__)
                finally:
                    if old_main is not None:
                        sys.modules['__main__'] = old_main