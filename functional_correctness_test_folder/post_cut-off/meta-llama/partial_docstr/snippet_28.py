
from typing import Optional, Dict, Any
from enum import Enum


class CostMode(Enum):
    # Assuming CostMode is an Enum, actual values are not provided
    DEFAULT = 1


class TokenCounts:
    # Assuming TokenCounts is a class, actual implementation is not provided
    def __init__(self, input_tokens: int, output_tokens: int, cache_creation_tokens: int = 0, cache_read_tokens: int = 0):
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        self.cache_creation_tokens = cache_creation_tokens
        self.cache_read_tokens = cache_read_tokens


MODEL_PRICING = {
    'model1': {
        'input': 0.01,
        'output': 0.02,
        'cache_creation': 0.005,
        'cache_read': 0.001
    },
    'model2': {
        'input': 0.02,
        'output': 0.03,
        'cache_creation': 0.01,
        'cache_read': 0.002
    }
    # Add more models as needed
}


class PricingCalculator:

    def __init__(self, custom_pricing: Optional[Dict[str, Dict[str, float]]] = None) -> None:
        '''Initialize with optional custom pricing.
        Args:
            custom_pricing: Optional custom pricing dictionary to override defaults.
                          Should follow same structure as MODEL_PRICING.
        '''
        self.pricing = MODEL_PRICING.copy()
        if custom_pricing:
            self.pricing.update(custom_pricing)

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

        cost = (input_tokens * pricing['input'] +
                output_tokens * pricing['output'] +
                cache_creation_tokens * pricing.get('cache_creation', 0) +
                cache_read_tokens * pricing.get('cache_read', 0))

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
        if model not in self.pricing:
            if strict:
                raise KeyError(f"Unknown model: {model}")
            else:
                # Fallback to a default model or some other logic
                model = 'model1'  # Default model

        return self.pricing[model]

    def calculate_cost_for_entry(self, entry_data: Dict[str, Any], mode: CostMode) -> float:
        '''Calculate cost for a single entry (backward compatibility).
        Args:
            entry_data: Entry data dictionary
            mode: Cost mode (for backward compatibility)
        Returns:
            Cost in USD
        '''
        # Assuming entry_data contains 'model', 'input_tokens', 'output_tokens', etc.
        # and mode is not used in the calculation
        model = entry_data['model']
        tokens = TokenCounts(
            entry_data['input_tokens'], entry_data['output_tokens'])
        return self.calculate_cost(model, tokens=tokens)
