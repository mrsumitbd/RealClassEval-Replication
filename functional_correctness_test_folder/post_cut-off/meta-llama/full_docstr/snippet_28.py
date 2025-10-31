
from typing import Optional, Dict, Any
from enum import Enum


class CostMode(Enum):
    # Assuming CostMode is an Enum with some values
    DEFAULT = 1
    CUSTOM = 2


class TokenCounts:
    # Assuming TokenCounts is a class with some attributes
    def __init__(self, input_tokens: int, output_tokens: int, cache_creation_tokens: int = 0, cache_read_tokens: int = 0):
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        self.cache_creation_tokens = cache_creation_tokens
        self.cache_read_tokens = cache_read_tokens


MODEL_PRICING = {
    'model1': {'input': 0.01, 'output': 0.02, 'cache_creation': 0.001, 'cache_read': 0.0005},
    'model2': {'input': 0.02, 'output': 0.03, 'cache_creation': 0.002, 'cache_read': 0.001},
    # Add more models as needed
}


class PricingCalculator:
    '''Calculates costs based on model pricing with caching support.
    This class provides methods for calculating costs for individual models/tokens
    as well as detailed cost breakdowns for collections of usage entries.
    It supports custom pricing configurations and caches calculations for performance.
    Features:
    - Configurable pricing (from config or custom)
    - Fallback hardcoded pricing for robustness
    - Caching for performance
    - Support for all token types including cache
    - Backward compatible with both APIs
    '''

    def __init__(self, custom_pricing: Optional[Dict[str, Dict[str, float]]] = None) -> None:
        '''Initialize with optional custom pricing.
        Args:
            custom_pricing: Optional custom pricing dictionary to override defaults.
                          Should follow same structure as MODEL_PRICING.
        '''
        self.custom_pricing = custom_pricing if custom_pricing else {}
        self.pricing_cache = {}

    def calculate_cost(self, model: str, input_tokens: int = 0, output_tokens: int = 0, cache_creation_tokens: int = 0, cache_read_tokens: int = 0, tokens: Optional[TokenCounts] = None, strict: bool = False) -> float:
        '''Calculate cost with flexible API supporting both signatures.
        Args:
            model: Model name
            input_tokens: Number of input tokens (ignored if tokens provided)
            output_tokens: Number of output tokens (ignored if tokens provided)
            cache_creation_tokens: Number of cache creation tokens
            cache_read_tokens: Number of cache read tokens
            tokens: Optional TokenCounts object (takes precedence)
        Returns:
            Total cost in USD
        '''
        if tokens:
            input_tokens = tokens.input_tokens
            output_tokens = tokens.output_tokens
            cache_creation_tokens = tokens.cache_creation_tokens
            cache_read_tokens = tokens.cache_read_tokens

        pricing = self._get_pricing_for_model(model, strict)

        cache_key = (model, input_tokens, output_tokens,
                     cache_creation_tokens, cache_read_tokens)
        if cache_key in self.pricing_cache:
            return self.pricing_cache[cache_key]

        cost = (input_tokens * pricing['input'] +
                output_tokens * pricing['output'] +
                cache_creation_tokens * pricing.get('cache_creation', 0) +
                cache_read_tokens * pricing.get('cache_read', 0))

        self.pricing_cache[cache_key] = cost
        return cost

    def _get_pricing_for_model(self, model: str, strict: bool = False) -> Dict[str, float]:
        '''Get pricing for a model with optional fallback logic.
        Args:
            model: Model name
            strict: If True, raise KeyError for unknown models
        Returns:
            Pricing dictionary with input/output/cache costs
        Raises:
            KeyError: If strict=True and model is unknown
        '''
        if model in self.custom_pricing:
            return self.custom_pricing[model]
        elif model in MODEL_PRICING:
            return MODEL_PRICING[model]
        else:
            if strict:
                raise KeyError(f"Unknown model: {model}")
            else:
                # Return default pricing or some fallback value
                return {'input': 0.0, 'output': 0.0, 'cache_creation': 0.0, 'cache_read': 0.0}

    def calculate_cost_for_entry(self, entry_data: Dict[str, Any], mode: CostMode) -> float:
        '''Calculate cost for a single entry (backward compatibility).
        Args:
            entry_data: Entry data dictionary
            mode: Cost mode (for backward compatibility)
        Returns:
            Cost in USD
        '''
        # Assuming entry_data contains 'model', 'input_tokens', 'output_tokens', etc.
        model = entry_data['model']
        input_tokens = entry_data.get('input_tokens', 0)
        output_tokens = entry_data.get('output_tokens', 0)
        cache_creation_tokens = entry_data.get('cache_creation_tokens', 0)
        cache_read_tokens = entry_data.get('cache_read_tokens', 0)

        return self.calculate_cost(model, input_tokens, output_tokens, cache_creation_tokens, cache_read_tokens)


# Example usage:
if __name__ == "__main__":
    calculator = PricingCalculator()
    cost = calculator.calculate_cost(
        'model1', input_tokens=100, output_tokens=200)
    print(f"Cost: {cost}")

    entry_data = {'model': 'model1', 'input_tokens': 100, 'output_tokens': 200}
    cost = calculator.calculate_cost_for_entry(entry_data, CostMode.DEFAULT)
    print(f"Cost for entry: {cost}")
