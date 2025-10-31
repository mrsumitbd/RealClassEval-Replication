class Component:

    def render(self):
        raise NotImplementedError()

    def __str__(self):
        return ''.join(self._get_chunks(self.render()))

    @classmethod
    def _get_chunks(cls, gen):
        for chunk in gen:
            if isinstance(chunk, Component):
                yield from cls._get_chunks(chunk.render())
            elif isinstance(chunk, str):
                yield chunk
            else:
                yield str(chunk)

    def __repr__(self):
        return f'<SQL: "{self}">'