
from typing import Optional, Dict, Any


class TokenCounts:
    # Assuming TokenCounts is a class with input_tokens, output_tokens, cache_creation_tokens, and cache_read_tokens attributes
    def __init__(self, input_tokens: int = 0, output_tokens: int = 0, cache_creation_tokens: int = 0, cache_read_tokens: int = 0):
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        self.cache_creation_tokens = cache_creation_tokens
        self.cache_read_tokens = cache_read_tokens


class CostMode:
    # Assuming CostMode is an Enum with certain modes
    def __init__(self, mode: str):
        self.mode = mode


class PricingCalculator:

    def __init__(self, custom_pricing: Optional[Dict[str, Dict[str, float]]] = None) -> None:
        self.custom_pricing = custom_pricing if custom_pricing is not None else {}
        self.default_pricing = {
            'model1': {'input': 0.01, 'output': 0.02, 'cache_creation': 0.005, 'cache_read': 0.001},
            'model2': {'input': 0.02, 'output': 0.03, 'cache_creation': 0.01, 'cache_read': 0.002},
            # Add more default models as needed
        }

    def calculate_cost(self, model: str, input_tokens: int = 0, output_tokens: int = 0, cache_creation_tokens: int = 0, cache_read_tokens: int = 0, tokens: Optional[TokenCounts] = None, strict: bool = False) -> float:
        if tokens is not None:
            input_tokens = tokens.input_tokens
            output_tokens = tokens.output_tokens
            cache_creation_tokens = tokens.cache_creation_tokens
            cache_read_tokens = tokens.cache_read_tokens

        pricing = self._get_pricing_for_model(model, strict)

        cost = (input_tokens * pricing.get('input', 0) +
                output_tokens * pricing.get('output', 0) +
                cache_creation_tokens * pricing.get('cache_creation', 0) +
                cache_read_tokens * pricing.get('cache_read', 0))

        return cost

    def _get_pricing_for_model(self, model: str, strict: bool = False) -> Dict[str, float]:
        if model in self.custom_pricing:
            return self.custom_pricing[model]
        elif model in self.default_pricing:
            return self.default_pricing[model]
        else:
            if strict:
                raise ValueError(f"Pricing for model '{model}' not found")
            else:
                return {'input': 0, 'output': 0, 'cache_creation': 0, 'cache_read': 0}

    def calculate_cost_for_entry(self, entry_data: Dict[str, Any], mode: CostMode) -> float:
        model = entry_data.get('model')
        if mode.mode == 'tokens':
            tokens = TokenCounts(**entry_data.get('tokens', {}))
            return self.calculate_cost(model, tokens=tokens)
        elif mode.mode == 'detailed':
            input_tokens = entry_data.get('input_tokens', 0)
            output_tokens = entry_data.get('output_tokens', 0)
            cache_creation_tokens = entry_data.get('cache_creation_tokens', 0)
            cache_read_tokens = entry_data.get('cache_read_tokens', 0)
            return self.calculate_cost(model, input_tokens, output_tokens, cache_creation_tokens, cache_read_tokens)
        else:
            raise ValueError(f"Unsupported cost mode: {mode.mode}")
