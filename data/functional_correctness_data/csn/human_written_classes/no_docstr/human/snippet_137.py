from actstream.models import Action, model_stream, user_stream, any_stream

class CustomStreamMixin:
    name = None

    def get_object(self):
        return

    def get_stream(self):
        return getattr(Action.objects, self.name)

    def items(self, *args, **kwargs):
        return self.get_stream()(*args[1:], **kwargs)