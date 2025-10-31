from globus_cli.login_manager import LoginManager

class LazyCurrentIdentity:

    def __init__(self, value: str | None) -> None:
        self._value = value

    def resolve(self, login_manager: LoginManager) -> str:
        if self._value is None:
            self._value = login_manager.get_current_identity_id()
        return str(self._value)