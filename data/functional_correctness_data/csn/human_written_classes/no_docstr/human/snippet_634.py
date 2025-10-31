class BuiltInTimer:
    sunrise = 161
    sunset = 162

    @staticmethod
    def valid(byte_value: int) -> bool:
        return byte_value == BuiltInTimer.sunrise or byte_value == BuiltInTimer.sunset

    @staticmethod
    def valtostr(pattern: int) -> str:
        for key, value in list(BuiltInTimer.__dict__.items()):
            if type(value) is int and value == pattern:
                return key.replace('_', ' ').title()
        raise ValueError(f'{pattern} must be 0xA1 or 0xA2')