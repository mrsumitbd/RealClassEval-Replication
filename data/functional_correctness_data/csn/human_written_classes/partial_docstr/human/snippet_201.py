from nonebot.command.argfilter import ValidateError

class BaseValidator:
    """INTERNAL API"""

    def __init__(self, message=None):
        self.message = message

    def raise_failure(self):
        raise ValidateError(self.message)