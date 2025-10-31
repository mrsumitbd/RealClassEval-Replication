
class HeaderManager:

    def __init__(self) -> None:
        self.headers = []

    def create_header(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> list[str]:
        self.headers = [f"Plan: {plan}", f"Timezone: {timezone}"]
        return self.headers
