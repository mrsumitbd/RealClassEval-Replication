from typing import Any, Dict, List, Optional
from rich.console import Console, RenderableType

class AdvancedCustomLimitDisplay:
    """Display component for session-based P90 limits from general_limit sessions."""

    def __init__(self, console: Console) -> None:
        self.console = console

    def _collect_session_data(self, blocks: Optional[List[Dict[str, Any]]]=None) -> Dict[str, Any]:
        """Collect session data and identify limit sessions."""
        if not blocks:
            return {'all_sessions': [], 'limit_sessions': [], 'current_session': {'tokens': 0, 'cost': 0.0, 'messages': 0}, 'total_sessions': 0, 'active_sessions': 0}
        all_sessions = []
        limit_sessions = []
        current_session = {'tokens': 0, 'cost': 0.0, 'messages': 0}
        active_sessions = 0
        for block in blocks:
            if block.get('isGap', False):
                continue
            session = {'tokens': block.get('totalTokens', 0), 'cost': block.get('costUSD', 0.0), 'messages': block.get('sentMessagesCount', 0)}
            if block.get('isActive', False):
                active_sessions += 1
                current_session = session
            elif session['tokens'] > 0:
                all_sessions.append(session)
                if self._is_limit_session(session):
                    limit_sessions.append(session)
        return {'all_sessions': all_sessions, 'limit_sessions': limit_sessions, 'current_session': current_session, 'total_sessions': len(all_sessions) + active_sessions, 'active_sessions': active_sessions}

    def _is_limit_session(self, session: Dict[str, Any]) -> bool:
        """Check if session hit a general limit."""
        tokens = session['tokens']
        from claude_monitor.core.plans import COMMON_TOKEN_LIMITS, LIMIT_DETECTION_THRESHOLD
        for limit in COMMON_TOKEN_LIMITS:
            if tokens >= limit * LIMIT_DETECTION_THRESHOLD:
                return True
        return False

    def _calculate_session_percentiles(self, sessions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate percentiles from session data."""
        if not sessions:
            return {'tokens': {'p50': 19000, 'p75': 66000, 'p90': 88000, 'p95': 110000}, 'costs': {'p50': 100.0, 'p75': 150.0, 'p90': 200.0, 'p95': 250.0}, 'messages': {'p50': 150, 'p75': 200, 'p90': 250, 'p95': 300}, 'averages': {'tokens': 19000, 'cost': 100.0, 'messages': 150}, 'count': 0}
        import numpy as np
        tokens = [s['tokens'] for s in sessions]
        costs = [s['cost'] for s in sessions]
        messages = [s['messages'] for s in sessions]
        return {'tokens': {'p50': int(np.percentile(tokens, 50)), 'p75': int(np.percentile(tokens, 75)), 'p90': int(np.percentile(tokens, 90)), 'p95': int(np.percentile(tokens, 95))}, 'costs': {'p50': float(np.percentile(costs, 50)), 'p75': float(np.percentile(costs, 75)), 'p90': float(np.percentile(costs, 90)), 'p95': float(np.percentile(costs, 95))}, 'messages': {'p50': int(np.percentile(messages, 50)), 'p75': int(np.percentile(messages, 75)), 'p90': int(np.percentile(messages, 90)), 'p95': int(np.percentile(messages, 95))}, 'averages': {'tokens': float(np.mean(tokens)), 'cost': float(np.mean(costs)), 'messages': float(np.mean(messages))}, 'count': len(sessions)}