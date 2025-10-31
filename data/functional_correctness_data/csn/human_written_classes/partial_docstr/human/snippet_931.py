import json

class RenderList:
    """Object that represents a list of renders."""

    def __init__(self, sdk, values):
        self.count = values.get('count')
        self.items = list(map(lambda x: Render(x), values.get('items', [])))

    def attrs(self):
        return {'count': self.count, 'items': map(Render.attrs, self.items)}

    def json(self):
        return json.dumps(self.attrs(), indent=4)