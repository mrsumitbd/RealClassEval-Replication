from elicitation import ElicitationField, ElicitationManager, ElicitationRequest, ElicitationResponse
from typing import Any, Dict, List, Optional

class ElicitationCache:
    """Cache for commonly used elicitation patterns."""

    def __init__(self, max_size: int=100):
        self.cache = {}
        self.max_size = max_size
        self.access_count = {}

    def get_cached_response(self, request_signature: str) -> Optional[Dict[str, Any]]:
        """Get cached response for similar requests."""
        if request_signature in self.cache:
            self.access_count[request_signature] = self.access_count.get(request_signature, 0) + 1
            return self.cache[request_signature]
        return None

    def cache_response(self, request_signature: str, response_values: Dict[str, Any]):
        """Cache a response for future use."""
        if len(self.cache) >= self.max_size:
            least_used = min(self.access_count, key=self.access_count.get)
            del self.cache[least_used]
            del self.access_count[least_used]
        self.cache[request_signature] = response_values
        self.access_count[request_signature] = 1

    def generate_signature(self, request: ElicitationRequest) -> str:
        """Generate a signature for caching purposes."""
        field_sigs = [f'{f.name}:{f.type}:{f.required}' for f in request.fields]
        return f"{request.type.value}:{request.title}:{':'.join(sorted(field_sigs))}"