class StringDecoderErr:
    """Errors related to string lexer"""

    @staticmethod
    def string_invalid_start(char: str) -> str:
        return f'Invalid start of string: <{char}>'

    @staticmethod
    def unexpected_end_of_string() -> str:
        return 'Unexpected end of string'

    @staticmethod
    def unexpected_escape_sequence(char: str) -> str:
        return f'Unexpected escape sequence: <{char}>'