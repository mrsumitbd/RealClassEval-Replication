from datetime import datetime

class OpenAIResponse:

    def __init__(self, data):
        for key, value in data.items():
            if isinstance(value, dict):
                value = OpenAIResponse(value)
            elif isinstance(value, list):
                value = [OpenAIResponse(item) if isinstance(item, dict) else item for item in value]
            setattr(self, key, value)

    def model_dump(self, *args, **kwargs):
        data = self.__dict__
        data['created_at'] = datetime.now().isoformat()
        return data