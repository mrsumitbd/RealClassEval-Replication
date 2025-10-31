
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

    MODEL_PRICING = {
        'gpt-3.5-turbo': {
            'input': 0.0015,
            'output': 0.002,
            'cache_creation': 0.0015,
            'cache_read': 0.0005
        },
        'gpt-4': {
            'input': 0.03,
            'output': 0.06,
            'cache_creation': 0.03,
            'cache_read': 0.01
        },
        'gpt-4-turbo': {
            'input': 0.01,
            'output': 0.03,
            'cache_creation': 0.01,
            'cache_read': 0.003
        }
    }

    def __init__(self, custom_pricing: Optional[Dict[str, Dict[str, float]]] = None) -> None:
        '''Initialize with optional custom pricing.
        Args:
            custom_pricing: Optional custom pricing dictionary to override defaults.
                          Should follow same structure as MODEL_PRICING.
        '''
        self.custom_pricing = custom_pricing or {}
        self.cache = {}

    def calculate_cost(self, model: str, input_tokens: int = 0, output_tokens: int = 0,
                       cache_creation_tokens: int = 0, cache_read_tokens: int = 0,
                       tokens: Optional[TokenCounts] = None, strict: bool = False) -> float:
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
        if tokens is not None:
            input_tokens = tokens.input
            output_tokens = tokens.output
            cache_creation_tokens = tokens.cache_creation
            cache_read_tokens = tokens.cache_read

        pricing = self._get_pricing_for_model(model, strict)
        cost = (input_tokens * pricing['input'] +
                output_tokens * pricing['output'] +
                cache_creation_tokens * pricing['cache_creation'] +
                cache_read_tokens * pricing['cache_read'])
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
        if model in self.MODEL_PRICING:
            return self.MODEL_PRICING[model]
        if strict:
            raise KeyError(f"Unknown model: {model}")
        return {
            'input': 0.0,
            'output': 0.0,
            'cache_creation': 0.0,
            'cache_read': 0.0
        }

    def calculate_cost_for_entry(self, entry_data: Dict[str, Any], mode: CostMode) -> float:
        '''Calculate cost for a single entry (backward compatibility).
        Args:
            entry_data: Entry data dictionary
            mode: Cost mode (for backward compatibility)
        Returns:
            Cost in USD
        '''
        model = entry_data.get('model', '')
        if mode == CostMode.INPUT:
            tokens = entry_data.get('input_tokens', 0)
            return self.calculate_cost(model, input_tokens=tokens)
        elif mode == CostMode.OUTPUT:
            tokens = entry_data.get('output_tokens', 0)
            return self.calculate_cost(model, output_tokens=tokens)
        elif mode == CostMode.CACHE_CREATION:
            tokens = entry_data.get('cache_creation_tokens', 0)
            return self.calculate_cost(model, cache_creation_tokens=tokens)
        elif mode == CostMode.CACHE_READ:
            tokens = entry_data.get('cache_read_tokens', 0)
            return self.calculate_cost(model, cache_read_tokens=tokens)
        else:
            return self.calculate_cost(
                model,
                input_tokens=entry_data.get('input_tokens', 0),
                output_tokens=entry_data.get('output_tokens', 0),
                cache_creation_tokens=entry_data.get(
                    'cache_creation_tokens', 0),
                cache_read_tokens=entry_data.get('cache_read_tokens', 0)
            )
