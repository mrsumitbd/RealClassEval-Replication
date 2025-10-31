class Fold:

    def __init__(self, name, description=None):
        self.fold_name = name
        self.description = description or name

    def __enter__(self):
        print('travis_fold:start:%s\x1b[33;1m%s\x1b[0m' % (self.fold_name, self.description), flush=True)

    def __exit__(self, exc_type, exc_value, traceback):
        print('\ntravis_fold:end:%s\r' % self.fold_name, end='', flush=True)