from typing import Any, Dict, List, Optional, Tuple
import random

class TextWorldChallengeRegistry:
    """Registry for pre-built TextWorld challenges."""
    CHALLENGES = {'tw-simple': {'rewards': ['sparse', 'balanced', 'dense'], 'goal': ['detailed', 'brief', 'none'], 'test': [False]}, 'tw-cooking': {'recipe': [1, 2, 3, 4], 'take': [1, 2, 3, 4], 'cook': [False, True], 'open': [False, True], 'drop': [False, True], 'go': [1, 6, 9, 12]}, 'tw-coin_collector': {'level': list(range(1, 301))}, 'tw-treasure_hunter': {'level': list(range(1, 31))}}
    ALL_CHALLENGES = list(CHALLENGES.keys())

    def __init__(self, seed: Optional[int]=None):
        self._challenges = self.CHALLENGES.copy()
        self.rng = random.Random(seed)
        self._all_combinations = None
        self._combination_index = 0

    def list_challenges(self) -> List[str]:
        """List all available pre-built challenges."""
        return list(self._challenges.keys())

    def get_random_challenge(self, randomize_settings: bool=True) -> Tuple[str, Dict[str, Any]]:
        """Get a random challenge with optionally randomized settings.

        Args:
            randomize_settings: Whether to randomize settings from available options

        Returns:
            Tuple of (challenge_name, settings_dict)
        """
        challenge_name = self.rng.choice(self.list_challenges())
        return self.get_challenge(challenge_name, randomize_settings)

    def get_challenge(self, name: str, randomize_settings: bool=True) -> Tuple[str, Dict[str, Any]]:
        """Get challenge name and settings (optionally randomized).

        Args:
            name: Challenge name
            randomize_settings: Whether to randomize settings from available options

        Returns:
            Tuple of (challenge_name, settings_dict)
        """
        if name not in self._challenges:
            raise ValueError(f'Unknown challenge: {name}. Available: {self.list_challenges()}')
        settings_ranges = self._challenges[name]
        settings = {}
        for key, options in settings_ranges.items():
            if randomize_settings and len(options) > 1:
                settings[key] = self.rng.choice(options)
            else:
                settings[key] = options[0]
        if name == 'tw-cooking' and randomize_settings:
            recipe_value = settings['recipe']
            valid_take_values = [t for t in settings_ranges['take'] if t <= recipe_value]
            settings['take'] = self.rng.choice(valid_take_values) if valid_take_values else 1
        settings['seed'] = self.rng.randint(0, 4294967295)
        if name == 'tw-cooking':
            settings['recipe-seed'] = self.rng.randint(0, 4294967295)
        return (name, settings)