
from typing import Optional


class ShortcutsCommand:

    def __init__(self):
        self.shortcuts = {}

    def run(self, shell: Optional[str] = None) -> int:
        # For demonstration purposes, assume we have a function to get shortcuts
        self.shortcuts = self._get_shortcuts(shell)
        self._print_result(self.shortcuts)
        return 0

    def _print_result(self, result: dict) -> None:
        for name, command in result.items():
            print(f"{name}: {command}")

    def _get_shortcuts(self, shell: Optional[str] = None) -> dict:
        # For demonstration purposes, assume we have some predefined shortcuts
        shortcuts = {
            "ll": "ls -l",
            "cp": "cp -i",
            "mv": "mv -i",
            "rm": "rm -i"
        }
        if shell == "bash":
            shortcuts[".."] = "cd .."
        elif shell == "zsh":
            shortcuts[".."] = "cd .. && ls"
        return shortcuts


# Example usage:
if __name__ == "__main__":
    command = ShortcutsCommand()
    command.run("bash")
