class Filter:

    def __init__(self, **kwargs):
        raise Exception('AbstractClass')

    def run(self, reader, writer):
        for block in reader:
            block = self(block)
            if block:
                writer(block)

    def step(self, reader, writer):
        block = next(reader)
        if not block:
            raise StopIteration
        block = self(block)
        if block:
            writer(block)

    def __call__(self, block):
        raise Exception('AbstractMethod')