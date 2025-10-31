import sys

class StatementHash:
    stmt_hash = {}

    def __init__(self) -> None:
        pass

    def hash(self, script: str) -> str:
        h = hash(script) & sys.maxsize
        StatementHash.stmt_hash[h] = script
        return f'script_{h}'

    def script(self, hash: str) -> str:
        return StatementHash.stmt_hash[int(hash[7:])]