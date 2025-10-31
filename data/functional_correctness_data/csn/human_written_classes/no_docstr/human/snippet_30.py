class BaseUser:

    @property
    def is_authenticated(self) -> bool:
        raise NotImplementedError()

    @property
    def display_name(self) -> str:
        raise NotImplementedError()

    @property
    def identity(self) -> str:
        raise NotImplementedError()