class Post:

    def __init__(self, url):
        self.url = url
        self.title = None
        self.comments = []

    def add_comment(self, comment):
        comment['id'] = len(self.comments) + 1
        self.comments.append(comment)