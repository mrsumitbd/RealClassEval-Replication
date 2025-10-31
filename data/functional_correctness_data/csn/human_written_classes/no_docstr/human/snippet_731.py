class PageIterator:

    def __init__(self, client, next_url, **options):
        self.__client = client
        self.__next_url = next_url
        self.__options = options
        self.__has_more = True

    def __iter__(self):
        return self

    def __next__(self):
        if self.__has_more:
            page = self.__client._make_request('GET', self.__next_url, None, **self.__options)
            if 'params' in self.__options:
                del self.__options['params']
            self.__next_url = page.next
            self.__has_more = page.has_more
            return page.data
        else:
            raise StopIteration