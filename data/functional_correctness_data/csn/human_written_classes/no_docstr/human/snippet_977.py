class ModuleData:

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.groups: dict[str, set[str]] = {'commands': set(), 'hooks': set()}
        self.disabled: dict[str, set[str]] = {'commands': set(), 'hooks': set()}
        self.aux: list[str] = []