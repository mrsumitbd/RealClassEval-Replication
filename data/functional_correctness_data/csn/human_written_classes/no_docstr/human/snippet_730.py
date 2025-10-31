class ItemIterator:

    def __init__(self, client, next_url, **options):
        self.__page_iterator = PageIterator(client, next_url, **options)
        self.__index = 0
        self.__data = None

    def __iter__(self):
        return self

    def __next__(self):
        if self.__data and self.__index < len(self.__data) - 1:
            self.__index += 1
        else:
            self.__data = next(self.__page_iterator)
            self.__index = 0
        if len(self.__data) > 0:
            return self.__data[self.__index]
        else:
            raise StopIteration