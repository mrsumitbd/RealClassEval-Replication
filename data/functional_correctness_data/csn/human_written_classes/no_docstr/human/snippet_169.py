class Summary:

    def __init__(self) -> None:
        self.summary: dict[str, int] = {}

    def update(self, wrongword: str) -> None:
        if wrongword in self.summary:
            self.summary[wrongword] += 1
        else:
            self.summary[wrongword] = 1

    def __str__(self) -> str:
        keys = list(self.summary.keys())
        keys.sort()
        return '\n'.join([f'{key}{self.summary.get(key):{15 - len(key)}}' for key in keys])