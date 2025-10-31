class FileFromGist:

    def __init__(self, name, gist, url, public):
        self.name = name
        self.gist = gist
        self.url = url
        self.public = public

    def __str__(self):
        if self.public:
            return self.name
        return '{} [Secret Gist]'.format(self.name)

    def __repr__(self):
        return str({'name': self.name, 'gist': self.gist, 'url': self.url, 'public': self.public})

    def __eq__(self, other):
        if self.name != other.name:
            return False
        if self.gist != other.gist:
            return False
        if self.url != other.url:
            return False
        if self.public != other.public:
            return False
        return True