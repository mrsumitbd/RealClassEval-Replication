from typing import Callable, List, Any, Optional, Dict

class EffectManager:
    """
    Centralized Effect Management.
    Effect management mechanism that allows to coordinate and control 
    the application's side effects in a centralized way, to ensure a 
    consistent and predictable execution of effects.
    """

    def __init__(self):
        self._effects: Dict[str, 'Effect'] = {}
        self._initialized = False

    def useEffect(self, effect_fn: Callable, dependencies: List[Any]=None, key: Optional[str]=None):
        """
        Registers an effect to trigger.
        Registers an effect that will be triggered on certain events or changes, 
        allowing to manage the application's side effects efficiently.

        args:
            effect_fn: Function to execute when the effect is triggered
            dependencies: Re-run the effect only if these dependencies change, to avoid unnecessary executions
            key: Unique key to identify the effect and manage it precisely
        """
        effect_key = key or f'effect_{len(self._effects)}'
        if effect_key not in self._effects:
            self._effects[effect_key] = Effect(effect_fn, dependencies)
        else:
            self._effects[effect_key].update(effect_fn, dependencies)

    def runEffects(self):
        """Runs all registered effects"""
        for effect in self._effects.values():
            effect.run()

    def dispose(self):
        """Cleans up all effects"""
        for effect in self._effects.values():
            effect.dispose()
        self._effects.clear()