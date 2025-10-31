
class HeaderManager:

    def __init__(self) -> None:
        pass

    def create_header(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> list[str]:
        return [
            f"X-Plan: {plan}",
            f"X-Timezone: {timezone}"
        ]
