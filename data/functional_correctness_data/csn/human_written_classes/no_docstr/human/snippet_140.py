from actstream.models import Action, model_stream, user_stream, any_stream

class UserActivityMixin:

    def get_object(self, request):
        if request.user.is_authenticated:
            return request.user

    def get_stream(self):
        return user_stream

    def get_stream_kwargs(self, request):
        stream_kwargs = {}
        if 'with_user_activity' in request.GET:
            stream_kwargs['with_user_activity'] = request.GET['with_user_activity'].lower() == 'true'
        return stream_kwargs