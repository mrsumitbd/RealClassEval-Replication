class BaseTokenGenerator:
    """
    Base Class for the Token Generators

    - Can take arbitrary args/kwargs and work with those
    - Needs to implement the "generate_token" Method
    """

    def __init__(self, *args, **kwargs):
        pass

    def generate_token(self, *args, **kwargs):
        raise NotImplementedError