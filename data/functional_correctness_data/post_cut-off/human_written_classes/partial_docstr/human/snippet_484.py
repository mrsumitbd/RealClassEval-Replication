from typing import Any, Callable, Dict, List, Optional, Type, Union
from datetime import datetime

class StandardErrorResponse:
    """Standardized error response format."""

    def __init__(self, error: Exception, context: Optional[Dict[str, Any]]=None):
        self.error = error
        self.context = context or {}
        self.timestamp = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format for JSON responses."""
        return {'error': {'type': type(self.error).__name__, 'message': str(self.error), 'timestamp': self.timestamp.isoformat(), 'context': self.context}, 'success': False}

    def to_string(self) -> str:
        """Convert to string format for text responses."""
        context_str = f' (Context: {self.context})' if self.context else ''
        return f'Error: {str(self.error)}{context_str}'