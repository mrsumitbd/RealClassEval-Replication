
from typing import List


class ErrorDisplayComponent:
    '''Error display component for handling error states.'''

    def __init__(self) -> None:
        pass

    def format_error_screen(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> List[str]:
        error_screen = [
            f"Error: Invalid plan '{plan}'",
            f"Timezone: {timezone}"
        ]
        return error_screen
