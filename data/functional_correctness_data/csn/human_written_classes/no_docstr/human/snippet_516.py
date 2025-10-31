import math
from txmongo._gridfs.errors import CorruptGridFile
from twisted.internet import defer

class GridOutIterator:

    def __init__(self, grid_out, chunks):
        self.__id = grid_out._id
        self.__chunks = chunks
        self.__current_chunk = 0
        self.__max_chunk = math.ceil(float(grid_out.length) / grid_out.chunk_size)

    def __iter__(self):
        return self

    def __next__(self):
        if self.__current_chunk >= self.__max_chunk:
            return defer.succeed(None)

        def ok(chunk):
            if not chunk:
                raise CorruptGridFile('TxMongo: no chunk #{0}'.format(self.__current_chunk))
            self.__current_chunk += 1
            return bytes(chunk['data'])
        return self.__chunks.find_one({'files_id': self.__id, 'n': self.__current_chunk}).addCallback(ok)
    next = __next__