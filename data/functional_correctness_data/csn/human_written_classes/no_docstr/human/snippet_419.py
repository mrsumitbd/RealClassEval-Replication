class CommentsProvider:

    def __init__(self, blog_page, entry_page):
        self.blog_page = blog_page
        self.entry_page = entry_page

    @property
    def template(self):
        raise NotImplementedError()

    def get_context(self):
        raise NotImplementedError()

    def get_num_comments(self):
        raise NotImplementedError()