
class HeaderManager:

    def __init__(self) -> None:
        pass

    def create_header(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> list[str]:
        headers = [
            f"Plan: {plan}",
            f"Timezone: {timezone}",
            "Content-Type: application/json",
            "Accept: application/json"
        ]
        return headers
