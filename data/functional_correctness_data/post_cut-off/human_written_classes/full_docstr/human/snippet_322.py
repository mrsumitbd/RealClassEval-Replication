from pathlib import Path
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import json

@dataclass
class SmartDefaultsConfig:
    """Configuration for Smart Defaults system"""
    enabled: bool = False
    enable_pattern_recognition: bool = True
    enable_learning: bool = True
    enable_field_suggestions: bool = True
    learning_storage_path: Path = field(default_factory=lambda: Path.home() / '.kafka-schema-mcp' / 'smart_defaults')
    learning_retention_days: int = 90
    minimum_occurrences_for_pattern: int = 2
    min_confidence_for_suggestion: float = 0.3
    min_confidence_for_auto_fill: float = 0.7
    high_confidence_threshold: float = 0.8
    pattern_detection_threshold: float = 0.4
    max_patterns_to_track: int = 50
    pattern_cache_ttl_seconds: int = 300
    anonymize_values: bool = False
    excluded_fields: List[str] = field(default_factory=lambda: ['password', 'secret', 'key', 'token', 'credential'])
    excluded_contexts: List[str] = field(default_factory=list)
    show_confidence_scores: bool = True
    show_suggestion_source: bool = True
    show_reasoning: bool = True
    max_field_suggestions: int = 10
    enable_caching: bool = True
    cache_size: int = 100
    async_learning: bool = True
    environment_defaults: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {'production': {'compatibility': 'FULL', 'dry_run': True, 'preserve_ids': True}, 'staging': {'compatibility': 'BACKWARD', 'dry_run': True, 'preserve_ids': True}, 'development': {'compatibility': 'NONE', 'dry_run': False, 'preserve_ids': False}})
    enable_multi_step_learning: bool = True
    suggestion_decay_factor: float = 0.95
    enable_cross_context_learning: bool = False

    @classmethod
    def from_env(cls) -> 'SmartDefaultsConfig':
        """Create configuration from environment variables"""
        config = cls()
        if os.getenv('SMART_DEFAULTS_ENABLED') is not None:
            config.enabled = os.getenv('SMART_DEFAULTS_ENABLED', '').lower() == 'true'
        if os.getenv('SMART_DEFAULTS_PATTERN_RECOGNITION') is not None:
            config.enable_pattern_recognition = os.getenv('SMART_DEFAULTS_PATTERN_RECOGNITION', '').lower() == 'true'
        if os.getenv('SMART_DEFAULTS_LEARNING') is not None:
            config.enable_learning = os.getenv('SMART_DEFAULTS_LEARNING', '').lower() == 'true'
        if os.getenv('SMART_DEFAULTS_FIELD_SUGGESTIONS') is not None:
            config.enable_field_suggestions = os.getenv('SMART_DEFAULTS_FIELD_SUGGESTIONS', '').lower() == 'true'
        if os.getenv('SMART_DEFAULTS_STORAGE_PATH'):
            config.learning_storage_path = Path(os.getenv('SMART_DEFAULTS_STORAGE_PATH'))
        if os.getenv('SMART_DEFAULTS_RETENTION_DAYS'):
            config.learning_retention_days = int(os.getenv('SMART_DEFAULTS_RETENTION_DAYS'))
        if os.getenv('SMART_DEFAULTS_MIN_CONFIDENCE'):
            config.min_confidence_for_suggestion = float(os.getenv('SMART_DEFAULTS_MIN_CONFIDENCE'))
        if os.getenv('SMART_DEFAULTS_AUTO_FILL_CONFIDENCE'):
            config.min_confidence_for_auto_fill = float(os.getenv('SMART_DEFAULTS_AUTO_FILL_CONFIDENCE'))
        if os.getenv('SMART_DEFAULTS_HIGH_CONFIDENCE_THRESHOLD'):
            config.high_confidence_threshold = float(os.getenv('SMART_DEFAULTS_HIGH_CONFIDENCE_THRESHOLD'))
        if os.getenv('SMART_DEFAULTS_ANONYMIZE') is not None:
            config.anonymize_values = os.getenv('SMART_DEFAULTS_ANONYMIZE', '').lower() == 'true'
        if os.getenv('SMART_DEFAULTS_EXCLUDED_FIELDS'):
            config.excluded_fields = os.getenv('SMART_DEFAULTS_EXCLUDED_FIELDS').split(',')
        if os.getenv('SMART_DEFAULTS_EXCLUDED_CONTEXTS'):
            config.excluded_contexts = os.getenv('SMART_DEFAULTS_EXCLUDED_CONTEXTS').split(',')
        if os.getenv('SMART_DEFAULTS_SHOW_CONFIDENCE') is not None:
            config.show_confidence_scores = os.getenv('SMART_DEFAULTS_SHOW_CONFIDENCE', '').lower() == 'true'
        if os.getenv('SMART_DEFAULTS_SHOW_REASONING') is not None:
            config.show_reasoning = os.getenv('SMART_DEFAULTS_SHOW_REASONING', '').lower() == 'true'
        if os.getenv('SMART_DEFAULTS_ENABLE_CACHING') is not None:
            config.enable_caching = os.getenv('SMART_DEFAULTS_ENABLE_CACHING', '').lower() == 'true'
        if os.getenv('SMART_DEFAULTS_CACHE_SIZE'):
            config.cache_size = int(os.getenv('SMART_DEFAULTS_CACHE_SIZE'))
        if os.getenv('SMART_DEFAULTS_MULTI_STEP_LEARNING') is not None:
            config.enable_multi_step_learning = os.getenv('SMART_DEFAULTS_MULTI_STEP_LEARNING', '').lower() == 'true'
        if os.getenv('SMART_DEFAULTS_CROSS_CONTEXT_LEARNING') is not None:
            config.enable_cross_context_learning = os.getenv('SMART_DEFAULTS_CROSS_CONTEXT_LEARNING', '').lower() == 'true'
        return config

    @classmethod
    def from_file(cls, config_path: Path) -> 'SmartDefaultsConfig':
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                data = json.load(f)
            if 'environment_defaults' in data:
                data['environment_defaults'] = data['environment_defaults']
            if 'learning_storage_path' in data:
                data['learning_storage_path'] = Path(data['learning_storage_path'])
            return cls(**data)
        except Exception as e:
            logger.error(f'Failed to load config from {config_path}: {e}')
            return cls()

    def to_file(self, config_path: Path):
        """Save configuration to JSON file"""
        try:
            data = {'enabled': self.enabled, 'enable_pattern_recognition': self.enable_pattern_recognition, 'enable_learning': self.enable_learning, 'enable_field_suggestions': self.enable_field_suggestions, 'learning_storage_path': str(self.learning_storage_path), 'learning_retention_days': self.learning_retention_days, 'minimum_occurrences_for_pattern': self.minimum_occurrences_for_pattern, 'min_confidence_for_suggestion': self.min_confidence_for_suggestion, 'min_confidence_for_auto_fill': self.min_confidence_for_auto_fill, 'high_confidence_threshold': self.high_confidence_threshold, 'pattern_detection_threshold': self.pattern_detection_threshold, 'max_patterns_to_track': self.max_patterns_to_track, 'pattern_cache_ttl_seconds': self.pattern_cache_ttl_seconds, 'anonymize_values': self.anonymize_values, 'excluded_fields': self.excluded_fields, 'excluded_contexts': self.excluded_contexts, 'show_confidence_scores': self.show_confidence_scores, 'show_suggestion_source': self.show_suggestion_source, 'show_reasoning': self.show_reasoning, 'max_field_suggestions': self.max_field_suggestions, 'enable_caching': self.enable_caching, 'cache_size': self.cache_size, 'async_learning': self.async_learning, 'environment_defaults': self.environment_defaults, 'enable_multi_step_learning': self.enable_multi_step_learning, 'suggestion_decay_factor': self.suggestion_decay_factor, 'enable_cross_context_learning': self.enable_cross_context_learning}
            config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(config_path, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info(f'Saved smart defaults config to {config_path}')
        except Exception as e:
            logger.error(f'Failed to save config to {config_path}: {e}')

    def validate(self) -> List[str]:
        """Validate configuration and return list of issues"""
        issues = []
        if not 0 <= self.min_confidence_for_suggestion <= 1:
            issues.append('min_confidence_for_suggestion must be between 0 and 1')
        if not 0 <= self.min_confidence_for_auto_fill <= 1:
            issues.append('min_confidence_for_auto_fill must be between 0 and 1')
        if not 0 <= self.high_confidence_threshold <= 1:
            issues.append('high_confidence_threshold must be between 0 and 1')
        if self.min_confidence_for_suggestion > self.min_confidence_for_auto_fill:
            issues.append('min_confidence_for_suggestion should be <= min_confidence_for_auto_fill')
        if not 0 <= self.pattern_detection_threshold <= 1:
            issues.append('pattern_detection_threshold must be between 0 and 1')
        if not 0 <= self.suggestion_decay_factor <= 1:
            issues.append('suggestion_decay_factor must be between 0 and 1')
        if self.learning_retention_days < 1:
            issues.append('learning_retention_days must be at least 1')
        if self.minimum_occurrences_for_pattern < 1:
            issues.append('minimum_occurrences_for_pattern must be at least 1')
        if self.max_patterns_to_track < 1:
            issues.append('max_patterns_to_track must be at least 1')
        if self.cache_size < 1:
            issues.append('cache_size must be at least 1')
        return issues

    def get_environment_defaults(self, environment: str) -> Dict[str, Any]:
        """Get defaults for a specific environment"""
        if environment in self.environment_defaults:
            return self.environment_defaults[environment]
        env_lower = environment.lower()
        for key, defaults in self.environment_defaults.items():
            if key.lower() in env_lower or env_lower in key.lower():
                return defaults
        return self.environment_defaults.get('development', {})

    def should_learn_from_field(self, field_name: str) -> bool:
        """Check if learning should be enabled for a field"""
        if not self.enable_learning:
            return False
        field_lower = field_name.lower()
        for excluded in self.excluded_fields:
            if excluded.lower() in field_lower:
                return False
        return True

    def should_learn_from_context(self, context: str) -> bool:
        """Check if learning should be enabled for a context"""
        if not self.enable_learning:
            return False
        return context not in self.excluded_contexts