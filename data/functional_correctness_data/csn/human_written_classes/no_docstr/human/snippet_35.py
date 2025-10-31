from tweepy.client import Response
import requests
from math import inf

class PaginationIterator:

    def __init__(self, method, *args, limit=inf, pagination_token=None, reverse=False, **kwargs):
        self.method = method
        self.args = args
        self.limit = limit
        self.kwargs = kwargs
        self.reverse = reverse
        if reverse:
            self.previous_token = pagination_token
            self.next_token = None
        else:
            self.previous_token = None
            self.next_token = pagination_token
        self.count = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.reverse:
            pagination_token = self.previous_token
        else:
            pagination_token = self.next_token
        if self.count >= self.limit or (self.count and pagination_token is None):
            raise StopIteration
        if self.method.__name__ in ('search_all_tweets', 'search_recent_tweets', 'get_all_tweets_count'):
            self.kwargs['next_token'] = pagination_token
        else:
            self.kwargs['pagination_token'] = pagination_token
        response = self.method(*self.args, **self.kwargs)
        if isinstance(response, Response):
            meta = response.meta
        elif isinstance(response, dict):
            meta = response.get('meta', {})
        elif isinstance(response, requests.Response):
            meta = response.json().get('meta', {})
        else:
            raise RuntimeError(f'Unknown {type(response)} return type for {self.method.__qualname__}')
        self.previous_token = meta.get('previous_token')
        self.next_token = meta.get('next_token')
        self.count += 1
        return response