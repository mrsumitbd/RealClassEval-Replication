class FeedObject:

    def __init__(self, rating_id, rating_name):
        self.rating_id = rating_id
        self.rating_name = rating_name

    @property
    def id(self):
        return self.rating_id

    @property
    def name(self):
        return self.rating_name