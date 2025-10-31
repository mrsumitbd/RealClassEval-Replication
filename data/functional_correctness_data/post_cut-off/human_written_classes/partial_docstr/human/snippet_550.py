class Android:

    def tap(self, x: int, y: int) -> str:
        """Simulate a tap on the screen at the given coordinates."""
        return f'Simulated tap at ({x}, {y})'

    def get_screen(self) -> str:
        """Simulate getting the current screen content."""
        return 'Simulated screen content as a string.'

    def type_text(self, text: str) -> str:
        """Simulate typing text."""
        return f"Simulated typing text: '{text}'"