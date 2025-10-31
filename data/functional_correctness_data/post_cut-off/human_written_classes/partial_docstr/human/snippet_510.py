class IdentifierDecoderErr:
    """Errors related to identifier lexer"""

    @staticmethod
    def invalid_start(char: str) -> str:
        return f'Invalid start of identifier: <{char}>'

    @staticmethod
    def invalid_char(character: str) -> str:
        return f'Invalid character in identifier: <{character}>'