
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any
import json
import os


@dataclass
class SmartDefaultsConfig:
    '''Configuration for Smart Defaults system'''
    @classmethod
    def from_env(cls) -> 'SmartDefaultsConfig':
        '''Create configuration from environment variables'''
        return cls()

    @classmethod
    def from_file(cls, config_path: Path) -> 'SmartDefaultsConfig':
        '''Load configuration from JSON file'''
        with open(config_path, 'r') as f:
            config_data = json.load(f)
        return cls(**config_data)

    def to_file(self, config_path: Path):
        '''Save configuration to JSON file'''
        with open(config_path, 'w') as f:
            json.dump(self.__dict__, f)

    def validate(self) -> List[str]:
        '''Validate configuration and return list of issues'''
        return []

    def get_environment_defaults(self, environment: str) -> Dict[str, Any]:
        '''Get defaults for a specific environment'''
        return {}

    def should_learn_from_field(self, field_name: str) -> bool:
        '''Check if learning should be enabled for a field'''
        return True

    def should_learn_from_context(self, context: str) -> bool:
        '''Check if learning should be enabled for a context'''
        return True
