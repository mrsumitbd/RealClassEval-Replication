from typing import Dict, Any, Optional
from datetime import datetime, timezone, timedelta


class SessionCalculator:

    def __init__(self) -> None:
        pass

    @staticmethod
    def _ensure_aware(dt: datetime) -> datetime:
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)

    @staticmethod
    def _parse_datetime(val: Any) -> Optional[datetime]:
        if val is None:
            return None
        if isinstance(val, datetime):
            return SessionCalculator._ensure_aware(val)
        if isinstance(val, (int, float)):
            return datetime.fromtimestamp(float(val), tz=timezone.utc)
        if isinstance(val, str):
            s = val.strip()
            if s.endswith("Z"):
                s = s[:-1] + "+00:00"
            try:
                dt = datetime.fromisoformat(s)
                return SessionCalculator._ensure_aware(dt)
            except Exception:
                raise ValueError(f"Unrecognized datetime string format: {val}")
        raise ValueError(f"Unsupported datetime type: {type(val)}")

    @staticmethod
    def _clamp_non_negative(x: Optional[float]) -> Optional[float]:
        if x is None:
            return None
        return max(0.0, float(x))

    @staticmethod
    def _get_expected_duration_seconds(session_data: Dict[str, Any]) -> Optional[float]:
        for key in (
            "expected_duration_seconds",
            "expected_seconds",
            "planned_duration_seconds",
            "planned_seconds",
            "target_duration_seconds",
        ):
            if key in session_data and session_data[key] is not None:
                try:
                    v = float(session_data[key])
                    return v if v >= 0 else 0.0
                except Exception:
                    pass
        return None

    def calculate_time_data(self, session_data: Dict[str, Any], current_time: datetime) -> Dict[str, Any]:
        if not isinstance(session_data, dict):
            raise TypeError("session_data must be a dict")

        now = self._ensure_aware(current_time)
        start = self._parse_datetime(session_data.get("start_time"))
        if start is None:
            raise ValueError("session_data must include 'start_time'")

        end = self._parse_datetime(session_data.get("end_time"))
        effective_end = end or now

        elapsed_seconds = (effective_end - start).total_seconds()
        elapsed_seconds = max(0.0, elapsed_seconds)

        is_active = end is None or end > now

        expected_duration = self._get_expected_duration_seconds(session_data)

        remaining_seconds: Optional[float] = None
        progress: Optional[float] = None

        if expected_duration is not None and expected_duration > 0:
            if is_active:
                remaining_seconds = max(
                    0.0, expected_duration - elapsed_seconds)
            else:
                remaining_seconds = max(
                    0.0, expected_duration - (end - start).total_seconds())
            progress = max(0.0, min(1.0, elapsed_seconds / expected_duration))

        return {
            "start_time": start,
            "end_time": end,
            "current_time": now,
            "elapsed_seconds": elapsed_seconds,
            "is_active": bool(is_active),
            "expected_duration_seconds": expected_duration,
            "remaining_seconds": remaining_seconds,
            "progress": progress,
        }

    def calculate_cost_predictions(self, session_data: Dict[str, Any], time_data: Dict[str, Any], cost_limit: Optional[float] = None) -> Dict[str, Any]:
        if not isinstance(session_data, dict):
            raise TypeError("session_data must be a dict")
        if not isinstance(time_data, dict):
            raise TypeError("time_data must be a dict")

        elapsed_seconds = float(time_data.get("elapsed_seconds") or 0.0)
        expected_duration = time_data.get("expected_duration_seconds")
        remaining_seconds = time_data.get("remaining_seconds")

        cost_per_second = session_data.get("cost_per_second")
        cost_per_token = session_data.get("cost_per_token")
        tokens_processed = session_data.get(
            "tokens_processed", session_data.get("token_count"))
        token_rate_per_second = session_data.get("token_rate_per_second")
        total_expected_tokens = session_data.get("total_expected_tokens")

        cps = float(cost_per_second) if cost_per_second is not None else None
        cpt = float(cost_per_token) if cost_per_token is not None else None

        # Cost so far via time
        cost_so_far_via_seconds: Optional[float] = None
        if cps is not None:
            cost_so_far_via_seconds = max(0.0, elapsed_seconds * cps)

        # Cost so far via tokens
        cost_so_far_via_tokens: Optional[float] = None
        if cpt is not None and tokens_processed is not None:
            try:
                tp = float(tokens_processed)
                cost_so_far_via_tokens = max(0.0, tp * cpt)
            except Exception:
                pass

        # Best estimate cost so far preference: tokens if available, else seconds
        if cost_so_far_via_tokens is not None:
            cost_so_far = cost_so_far_via_tokens
        elif cost_so_far_via_seconds is not None:
            cost_so_far = cost_so_far_via_seconds
        else:
            cost_so_far = 0.0

        # Determine current cost rate per second
        cost_rate_per_second: Optional[float] = None
        if cps is not None:
            cost_rate_per_second = max(0.0, cps)
        elif cpt is not None and token_rate_per_second is not None:
            try:
                tr = float(token_rate_per_second)
                cost_rate_per_second = max(0.0, cpt * tr)
            except Exception:
                pass

        # Predicted totals
        predicted_total_cost: Optional[float] = None
        predicted_additional_cost: Optional[float] = None

        if expected_duration is not None:
            try:
                exp = float(expected_duration)
            except Exception:
                exp = None

            # Prefer token-based prediction if tokens expectation is known
            tokens_expected: Optional[float] = None
            if total_expected_tokens is not None:
                try:
                    tokens_expected = float(total_expected_tokens)
                except Exception:
                    tokens_expected = None
            elif token_rate_per_second is not None and exp is not None:
                try:
                    tokens_expected = float(token_rate_per_second) * exp
                except Exception:
                    tokens_expected = None

            pred_token_cost: Optional[float] = None
            if cpt is not None and tokens_expected is not None:
                pred_token_cost = max(0.0, cpt * tokens_expected)

            pred_time_cost: Optional[float] = None
            if cps is not None and exp is not None:
                pred_time_cost = max(0.0, cps * exp)

            # Choose best prediction: prefer token-based if available
            if pred_token_cost is not None:
                predicted_total_cost = pred_token_cost
            elif pred_time_cost is not None:
                predicted_total_cost = pred_time_cost

            if predicted_total_cost is not None:
                predicted_additional_cost = max(
                    0.0, predicted_total_cost - cost_so_far)

        # Limit analysis
        will_exceed_limit: Optional[bool] = None
        seconds_until_limit: Optional[float] = None
        remaining_budget: Optional[float] = None

        if cost_limit is not None:
            try:
                limit = float(cost_limit)
            except Exception:
                limit = None
            if limit is not None and limit >= 0:
                remaining_budget = max(0.0, limit - cost_so_far)
                if predicted_total_cost is not None:
                    will_exceed_limit = predicted_total_cost > limit
                elif cost_rate_per_second is not None and cost_rate_per_second > 0:
                    # Estimate if continuing at current rate indefinitely
                    will_exceed_limit = True if remaining_budget == 0 else None
                else:
                    will_exceed_limit = None

                if cost_rate_per_second is not None and cost_rate_per_second > 0:
                    seconds_until_limit = max(
                        0.0, remaining_budget / cost_rate_per_second)
                else:
                    seconds_until_limit = None

        return {
            "cost_so_far": cost_so_far,
            "cost_so_far_via_seconds": cost_so_far_via_seconds,
            "cost_so_far_via_tokens": cost_so_far_via_tokens,
            "current_cost_rate_per_second": cost_rate_per_second,
            "predicted_total_cost": predicted_total_cost,
            "predicted_additional_cost": predicted_additional_cost,
            "remaining_budget": remaining_budget,
            "seconds_until_limit": seconds_until_limit,
            "will_exceed_limit": will_exceed_limit,
        }
