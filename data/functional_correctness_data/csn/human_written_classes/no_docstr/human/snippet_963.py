from copy import copy

class Entry:

    def __init__(self, request, response, result, arguments):
        self.request = request
        self.response = response
        self.result = result
        self.arguments = arguments

    @staticmethod
    def create(*args, response=None, arguments=None, **kwargs):
        return Entry(request=Request(*args, **kwargs), response=response, result=Result(), arguments=arguments or {})

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __copy__(self):
        return Entry(request=copy(self.request), response=copy(self.response), result=copy(self.result), arguments=copy(self.arguments))