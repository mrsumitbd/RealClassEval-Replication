
from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class Agent:
    name: str
    version: str
    capabilities: list[str]


@dataclass
class SessionAgent:
    name: str
    version: str
    capabilities: list[str] = field(default_factory=list)

    @classmethod
    def from_agent(cls, agent: 'Agent') -> 'SessionAgent':
        return cls(name=agent.name, version=agent.version, capabilities=agent.capabilities)

    @classmethod
    def from_dict(cls, env: dict[str, Any]) -> 'SessionAgent':
        return cls(name=env.get('name', ''), version=env.get('version', ''), capabilities=env.get('capabilities', []))

    def to_dict(self) -> dict[str, Any]:
        return {
            'name': self.name,
            'version': self.version,
            'capabilities': self.capabilities
        }
