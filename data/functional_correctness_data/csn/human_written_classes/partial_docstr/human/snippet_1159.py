class APIRequest:
    """Data Class for this library"""

    def __init__(self, url, api_name, api_value, shards, version, custom_headers, use_post, post_data):
        self.url = url
        self.api_name = api_name
        self.api_value = api_value
        self.shards = shards
        self.version = version
        self.custom_headers = custom_headers
        self.use_post = use_post
        self.post_data = post_data

    def __repr__(self):
        return str(vars(self))