from datetime import datetime

class L1VersionDTO:

    def __init__(self, version: int, status: str, description: str, create_time: datetime):
        self.version = version
        self.status = status
        self.description = description
        self.create_time = create_time

    @classmethod
    def from_model(cls, model: 'L1Version') -> 'L1VersionDTO':
        return cls(version=model.version, status=model.status, description=model.description, create_time=model.create_time)