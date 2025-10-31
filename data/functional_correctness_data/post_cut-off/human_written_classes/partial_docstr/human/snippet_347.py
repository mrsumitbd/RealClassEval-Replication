import os

class SSHKey:
    """
    Lightweight representation of a generated/known SSH key.
    """

    def __init__(self, private_path: str):
        self.private_path = private_path
        self.public_path = f'{private_path}.pub'

    def __str__(self) -> str:
        return os.path.basename(self.private_path)