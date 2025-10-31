class ConditionalRender:

    def __init__(self):
        self.mglo = None
        raise TypeError()

    def __enter__(self):
        self.mglo.begin_render()
        return self

    def __exit__(self, *args):
        self.mglo.end_render()