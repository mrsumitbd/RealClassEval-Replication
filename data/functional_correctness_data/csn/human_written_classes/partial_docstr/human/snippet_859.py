from json import dumps

class SampleExtension:
    """Here's an example of how to catch an annotation like this as a view handler."""

    def start(self, context):
        context.view.register(tuple, self.render_json)

    def render_json(self, context, result):
        if len(result) != 2 or result[0] != 'json':
            return
        resp = context.response
        resp.content_type = 'application/json'
        resp.encoding = 'utf-8'
        resp.text = dumps(result[1])
        return True