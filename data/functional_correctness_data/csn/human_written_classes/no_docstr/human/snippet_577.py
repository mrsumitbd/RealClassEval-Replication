class User:

    def __init__(self, id, username, password):
        setattr(self, 'user_id', id)
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.user_id

    def serialized(self):
        output = [getattr(self, 'user_id'), self.username, self.password, getattr(self, 'refresh_token', '')]
        return output

    def __json__(self):
        return {'user_id': self.user_id}