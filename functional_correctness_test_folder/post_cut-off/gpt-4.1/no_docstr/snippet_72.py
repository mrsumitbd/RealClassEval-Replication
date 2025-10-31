
from dataclasses import dataclass
from typing import Any


@dataclass
class SessionAgent:
    id: str
    name: str
    role: str

    @classmethod
    def from_agent(cls, agent: 'Agent') -> 'SessionAgent':
        return cls(id=agent.id, name=agent.name, role=agent.role)

    @classmethod
    def from_dict(cls, env: dict[str, Any]) -> 'SessionAgent':
        return cls(
            id=env['id'],
            name=env['name'],
            role=env['role']
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'role': self.role
        }
