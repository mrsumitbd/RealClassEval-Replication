from os.path import exists, join

class CacheFileMapper:

    def __init__(self, directory):
        self.directory = directory

    def get(self, token):
        return join(self.directory, token)