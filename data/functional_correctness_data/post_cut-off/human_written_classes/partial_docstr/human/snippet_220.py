from typing import Any, Dict, List

class MetricsTracker:
    """
    Track and analyze metrics over time
    """

    def __init__(self):
        self.metrics_history = {}

    def add_metrics(self, session_id: str, metrics: Dict[str, Any]) -> None:
        """Add metrics for a session"""
        if session_id not in self.metrics_history:
            self.metrics_history[session_id] = []
        metrics_with_time = metrics.copy()
        metrics_with_time['timestamp'] = timestamp()
        self.metrics_history[session_id].append(metrics_with_time)

    def get_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Get metrics history for a session"""
        return self.metrics_history.get(session_id, [])

    def get_average_metrics(self, session_id: str) -> Dict[str, float]:
        """Get average metrics for a session"""
        history = self.get_history(session_id)
        if not history:
            return {}
        result = {k: 0 for k in history[0] if isinstance(history[0][k], (int, float)) and k != 'timestamp'}
        for metrics in history:
            for k in result:
                if k in metrics and isinstance(metrics[k], (int, float)):
                    result[k] += metrics[k]
        count = len(history)
        for k in result:
            result[k] /= count
        return result