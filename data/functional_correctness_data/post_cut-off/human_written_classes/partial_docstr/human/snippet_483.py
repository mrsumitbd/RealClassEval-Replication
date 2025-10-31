from typing import Any, Callable, Dict, List, Optional, Type, Union
from datetime import datetime

class ErrorAggregator:
    """Aggregate multiple errors for batch operations."""

    def __init__(self):
        self.errors: List[Dict[str, Any]] = []

    def add_error(self, error: Exception, context: Optional[Dict[str, Any]]=None):
        """Add an error to the aggregator."""
        self.errors.append({'error_type': type(error).__name__, 'error_message': str(error), 'context': context or {}, 'timestamp': datetime.utcnow().isoformat()})

    def has_errors(self) -> bool:
        """Check if any errors have been recorded."""
        return len(self.errors) > 0

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of all errors."""
        if not self.errors:
            return {'error_count': 0, 'errors': []}
        error_types = {}
        for error in self.errors:
            error_type = error['error_type']
            error_types[error_type] = error_types.get(error_type, 0) + 1
        return {'error_count': len(self.errors), 'error_types': error_types, 'errors': self.errors}

    def raise_if_errors(self, aggregate_message: str='Multiple errors occurred'):
        """Raise an exception if any errors have been recorded."""
        if self.errors:
            summary = self.get_summary()
            raise WazuhMCPError(f'{aggregate_message}: {summary}')