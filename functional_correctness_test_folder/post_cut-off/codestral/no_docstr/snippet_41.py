
class HeaderManager:

    def __init__(self) -> None:
        self.headers = []

    def create_header(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> list[str]:
        self.headers = [
            f"X-Plan: {plan}",
            f"X-Timezone: {timezone}"
        ]
        return self.headers
