
from typing import Dict, Any, Optional
from datetime import datetime, timedelta


class SessionCalculator:

    def __init__(self) -> None:
        pass

    def calculate_time_data(self, session_data: Dict[str, Any], current_time: datetime) -> Dict[str, Any]:
        start_time = session_data.get('start_time')
        end_time = session_data.get('end_time')
        duration = None
        elapsed = None
        remaining = None

        if start_time and isinstance(start_time, datetime):
            if end_time and isinstance(end_time, datetime):
                duration = end_time - start_time
                elapsed = min(current_time, end_time) - start_time
                remaining = max(timedelta(0), end_time - current_time)
            else:
                elapsed = current_time - start_time
                duration = None
                remaining = None
        return {
            'start_time': start_time,
            'end_time': end_time,
            'duration': duration,
            'elapsed': elapsed,
            'remaining': remaining
        }

    def calculate_cost_predictions(self, session_data: Dict[str, Any], time_data: Dict[str, Any], cost_limit: Optional[float] = None) -> Dict[str, Any]:
        rate_per_hour = session_data.get('rate_per_hour', 0.0)
        elapsed = time_data.get('elapsed')
        duration = time_data.get('duration')
        predicted_total_cost = None
        cost_so_far = None
        time_to_limit = None
        limit_reached = False

        if elapsed and isinstance(elapsed, timedelta):
            hours_elapsed = elapsed.total_seconds() / 3600
            cost_so_far = hours_elapsed * rate_per_hour
        else:
            cost_so_far = 0.0

        if duration and isinstance(duration, timedelta):
            hours_total = duration.total_seconds() / 3600
            predicted_total_cost = hours_total * rate_per_hour
        else:
            predicted_total_cost = None

        if cost_limit is not None and rate_per_hour > 0:
            if cost_so_far >= cost_limit:
                time_to_limit = timedelta(0)
                limit_reached = True
            else:
                hours_left = (cost_limit - cost_so_far) / rate_per_hour
                time_to_limit = timedelta(hours=hours_left)
                if duration and isinstance(duration, timedelta):
                    remaining = duration - elapsed
                    if time_to_limit > remaining:
                        time_to_limit = remaining
        else:
            time_to_limit = None

        return {
            'cost_so_far': cost_so_far,
            'predicted_total_cost': predicted_total_cost,
            'time_to_limit': time_to_limit,
            'limit_reached': limit_reached
        }
