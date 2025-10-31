from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Union


class SessionCalculator:
    def __init__(self) -> None:
        self.default_cost_limit = 100.0

    def _to_datetime(self, value: Union[str, datetime, int, float, None]) -> Optional[datetime]:
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        if isinstance(value, (int, float)):
            # assume unix timestamp seconds
            return datetime.fromtimestamp(value)
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except Exception:
                # attempt RFC3339-like by replacing Z
                try:
                    return datetime.fromisoformat(value.replace("Z", "+00:00"))
                except Exception:
                    return None
        return None

    def _seconds(self, value: Optional[Union[int, float, timedelta]]) -> Optional[float]:
        if value is None:
            return None
        if isinstance(value, timedelta):
            return value.total_seconds()
        try:
            return float(value)
        except Exception:
            return None

    def calculate_time_data(self, session_data: Dict[str, Any], current_time: datetime) -> Dict[str, Any]:
        start_dt = self._to_datetime(session_data.get("start_time"))
        end_dt = self._to_datetime(session_data.get("end_time"))
        last_activity_dt = self._to_datetime(
            session_data.get("last_activity_time"))
        expected_duration_s = self._seconds(
            session_data.get("expected_duration_seconds"))

        now = current_time

        # Fallbacks
        if start_dt is None:
            start_dt = now
        if last_activity_dt is None:
            last_activity_dt = end_dt or now

        # Basic durations
        if end_dt and end_dt < start_dt:
            # sanitize swapped times
            start_dt, end_dt = end_dt, start_dt

        active = end_dt is None
        total_elapsed_s = ((now if active else end_dt) -
                           start_dt).total_seconds()
        if total_elapsed_s < 0:
            total_elapsed_s = 0.0

        idle_timeout_s = self._seconds(
            session_data.get("idle_timeout_seconds"))
        idle_seconds = (now - last_activity_dt).total_seconds()
        if idle_seconds < 0:
            idle_seconds = 0.0

        idle_exceeded = False
        if idle_timeout_s is not None:
            idle_exceeded = idle_seconds > idle_timeout_s
            # If idle exceeded and no explicit end, mark not active
            if active and idle_exceeded:
                active = False

        remaining_seconds = None
        predicted_end_time = None
        if expected_duration_s is not None:
            remaining_seconds = max(0.0, expected_duration_s - total_elapsed_s)
            predicted_end_time = start_dt + \
                timedelta(seconds=expected_duration_s)

        return {
            "now": now,
            "start_time": start_dt,
            "end_time": end_dt,
            "last_activity_time": last_activity_dt,
            "is_active": active,
            "elapsed_seconds": total_elapsed_s,
            "idle_seconds": idle_seconds,
            "idle_timeout_seconds": idle_timeout_s,
            "idle_exceeded": idle_exceeded,
            "expected_duration_seconds": expected_duration_s,
            "remaining_seconds": remaining_seconds,
            "predicted_end_time": predicted_end_time,
        }

    def _cost_rate_per_second(self, session_data: Dict[str, Any]) -> float:
        # direct rates
        for key, scale in (
            ("cost_per_second", 1.0),
            ("cost_per_minute", 1.0 / 60.0),
            ("cost_per_hour", 1.0 / 3600.0),
        ):
            v = session_data.get(key)
            if v is not None:
                try:
                    return float(v) * scale
                except Exception:
                    pass

        # derived rates
        events_per_second = session_data.get("events_per_second")
        avg_cost_per_event = session_data.get("average_cost_per_event")
        if events_per_second is not None and avg_cost_per_event is not None:
            try:
                return float(events_per_second) * float(avg_cost_per_event)
            except Exception:
                pass

        tokens_per_second = session_data.get("tokens_per_second")
        cost_per_token = session_data.get("cost_per_token")
        if tokens_per_second is not None and cost_per_token is not None:
            try:
                return float(tokens_per_second) * float(cost_per_token)
            except Exception:
                pass

        return 0.0

    def calculate_cost_predictions(
        self,
        session_data: Dict[str, Any],
        time_data: Dict[str, Any],
        cost_limit: Optional[float] = None,
    ) -> Dict[str, Any]:
        if cost_limit is None:
            cost_limit = self.default_cost_limit

        rate_per_second = self._cost_rate_per_second(session_data)

        base_cost = 0.0
        for key in ("accumulated_cost", "base_cost", "initial_cost", "spent_cost"):
            v = session_data.get(key)
            if v is not None:
                try:
                    base_cost = float(v)
                    break
                except Exception:
                    continue

        elapsed_seconds = float(time_data.get("elapsed_seconds", 0.0) or 0.0)
        now = time_data.get("now") or datetime.now()
        is_active = bool(time_data.get("is_active", False))
        expected_duration_s = time_data.get("expected_duration_seconds")

        spent_cost = base_cost + rate_per_second * elapsed_seconds
        burn_rate_per_hour = rate_per_second * 3600.0

        remaining_budget = None
        time_to_limit_seconds = None
        estimated_time_to_limit = None
        estimated_end_time_at_limit = None
        safe_within_limit = None

        if cost_limit is not None:
            remaining_budget = cost_limit - spent_cost
            safe_within_limit = remaining_budget >= 0.0
            if rate_per_second > 0 and is_active:
                if remaining_budget > 0:
                    time_to_limit_seconds = remaining_budget / rate_per_second
                    estimated_time_to_limit = timedelta(
                        seconds=time_to_limit_seconds)
                    estimated_end_time_at_limit = now + estimated_time_to_limit
                else:
                    time_to_limit_seconds = 0.0
                    estimated_time_to_limit = timedelta(seconds=0)
                    estimated_end_time_at_limit = now

        projected_total_cost = None
        if expected_duration_s is not None:
            total_cost_at_expected_end = base_cost + \
                rate_per_second * float(expected_duration_s)
            projected_total_cost = total_cost_at_expected_end

        return {
            "rate_per_second": rate_per_second,
            "burn_rate_per_hour": burn_rate_per_hour,
            "base_cost": base_cost,
            "spent_cost": spent_cost,
            "cost_limit": cost_limit,
            "remaining_budget": remaining_budget,
            "time_to_limit_seconds": time_to_limit_seconds,
            "estimated_time_to_limit": estimated_time_to_limit,
            "estimated_end_time_at_limit": estimated_end_time_at_limit,
            "projected_total_cost": projected_total_cost,
            "safe_within_limit": safe_within_limit,
        }
