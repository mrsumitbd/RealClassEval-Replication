from typing import Any, Dict, Optional, List, Union
from datetime import datetime, timezone, timedelta


class SessionCalculator:
    """Handles session-related calculations for display purposes.
    (Moved from ui/calculators.py)"""

    def __init__(self) -> None:
        """Initialize session calculator."""
        self.default_cost_limit = 100.0
        self._running_statuses = {
            "running", "active", "started", "starting", "initializing", "pending", "provisioning", "up"
        }
        self._stopped_statuses = {
            "stopped", "terminated", "failed", "completed", "succeeded", "finished",
            "canceled", "cancelled", "error", "inactive", "deleting", "deleted", "down", "stopping"
        }

    def _to_utc_datetime(self, value: Any) -> Optional[datetime]:
        if value is None:
            return None
        if isinstance(value, datetime):
            if value.tzinfo is None:
                return value.replace(tzinfo=timezone.utc)
            return value.astimezone(timezone.utc)
        if isinstance(value, (int, float)):
            try:
                return datetime.fromtimestamp(float(value), tz=timezone.utc)
            except Exception:
                return None
        if isinstance(value, str):
            s = value.strip()
            if not s:
                return None
            # Try POSIX timestamp string
            try:
                return datetime.fromtimestamp(float(s), tz=timezone.utc)
            except Exception:
                pass
            # Try ISO 8601
            try:
                if s.endswith("Z"):
                    s = s[:-1] + "+00:00"
                return datetime.fromisoformat(s).astimezone(timezone.utc)
            except Exception:
                return None
        return None

    def _get_first(self, data: Dict[str, Any], keys: List[str], default: Any = None) -> Any:
        for k in keys:
            if k in data and data[k] is not None:
                return data[k]
        return default

    def _parse_time_limit_seconds(self, data: Dict[str, Any]) -> Optional[int]:
        # Seconds keys
        sec = self._get_first(
            data,
            [
                "time_limit_seconds", "timeLimitSeconds", "max_duration_seconds", "maxDurationSeconds",
                "ttl_seconds", "ttlSeconds", "duration_limit_seconds", "durationLimitSeconds",
                "auto_stop_seconds", "autoStopSeconds", "maxRuntimeSeconds"
            ],
            None,
        )
        if isinstance(sec, (int, float)):
            return int(max(0, sec))
        # Hours keys
        hrs = self._get_first(
            data,
            ["time_limit_hours", "timeLimitHours",
                "max_duration_hours", "maxDurationHours"],
            None,
        )
        if isinstance(hrs, (int, float)):
            return int(max(0, float(hrs) * 3600))
        return None

    def _sum_pause_seconds(self, data: Dict[str, Any], start_dt: datetime, ref_end_dt: datetime) -> int:
        total = 0.0
        # Simple aggregate fields
        for key in ["paused_seconds", "total_paused_seconds", "pause_seconds", "accumulated_paused_seconds"]:
            v = data.get(key)
            if isinstance(v, (int, float)):
                # prefer the largest aggregate if multiple present
                total = max(total, float(v))

        # Intervals
        intervals = self._get_first(
            data, ["pause_intervals", "paused_intervals", "pauseIntervals"], [])
        if isinstance(intervals, list):
            for it in intervals:
                try:
                    if isinstance(it, dict):
                        s = self._to_utc_datetime(it.get("start") or it.get(
                            "start_time") or it.get("started_at"))
                        e = self._to_utc_datetime(it.get("end") or it.get(
                            "end_time") or it.get("ended_at") or it.get("stop_time"))
                    elif isinstance(it, (list, tuple)) and len(it) >= 1:
                        s = self._to_utc_datetime(it[0])
                        e = self._to_utc_datetime(
                            it[1]) if len(it) > 1 else None
                    else:
                        continue
                    if s is None:
                        continue
                    if e is None:
                        e = ref_end_dt
                    # Clip to [start_dt, ref_end_dt]
                    s_clamped = max(s, start_dt)
                    e_clamped = min(e, ref_end_dt)
                    if e_clamped > s_clamped:
                        total += (e_clamped - s_clamped).total_seconds()
                except Exception:
                    continue
        return int(max(0, total))

    def _format_hms(self, seconds: int) -> str:
        seconds = max(0, int(seconds))
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    def calculate_time_data(self, session_data: Dict[str, Any], current_time: datetime) -> Dict[str, Any]:
        """Calculate time-related data for the session.
        Args:
            session_data: Dictionary containing session information
            current_time: Current UTC time
        Returns:
            Dictionary with calculated time data
        """
        now = self._to_utc_datetime(current_time) or datetime.now(timezone.utc)

        start_dt = self._to_utc_datetime(
            self._get_first(
                session_data,
                ["start_time", "started_at", "startTime",
                    "created_at", "createdAt", "creation_time"],
                None,
            )
        )
        end_dt = self._to_utc_datetime(
            self._get_first(
                session_data,
                [
                    "end_time", "ended_at", "finished_at", "completed_at", "stop_time",
                    "stopped_at", "terminated_at", "endTime"
                ],
                None,
            )
        )

        status_raw = self._get_first(
            session_data, ["status", "state", "phase"], "")
        status = str(status_raw).strip().lower()

        if status in self._stopped_statuses:
            is_running = False
        elif status in self._running_statuses:
            is_running = True
        else:
            # Fallback to presence of end time
            is_running = end_dt is None or end_dt > now

        # If we know it's not running but no end time, use now as reference end
        ref_end_dt = end_dt if (end_dt is not None and not is_running) else now

        if start_dt is None:
            return {
                "start_time": None,
                "end_time": end_dt if not is_running else None,
                "status": status or None,
                "is_running": False,
                "wall_seconds": 0,
                "total_paused_seconds": 0,
                "active_seconds": 0,
                "active_hms": "00:00:00",
                "time_limit_seconds": self._parse_time_limit_seconds(session_data),
                "time_remaining_seconds": None,
                "estimated_end_time": None,
                "reference_end_time": ref_end_dt,
            }

        wall_seconds = int(max(0.0, (ref_end_dt - start_dt).total_seconds()))
        total_paused_seconds = self._sum_pause_seconds(
            session_data, start_dt, ref_end_dt)
        active_seconds = int(max(0, wall_seconds - total_paused_seconds))

        # If an explicit accumulated active time exists, prefer the larger (to avoid undercounting)
        explicit_active = self._get_first(
            session_data,
            ["active_seconds", "accumulated_active_seconds",
                "uptime_seconds", "runtime_seconds"],
            None,
        )
        if isinstance(explicit_active, (int, float)):
            active_seconds = max(active_seconds, int(explicit_active))

        time_limit_seconds = self._parse_time_limit_seconds(session_data)

        time_remaining_seconds: Optional[int]
        estimated_end_time: Optional[datetime]
        if time_limit_seconds is None:
            time_remaining_seconds = None
            estimated_end_time = end_dt if not is_running else None
        else:
            remaining = max(0, time_limit_seconds - active_seconds)
            time_remaining_seconds = int(remaining)
            # Approximate estimated end time for running sessions as now + remaining active time
            estimated_end_time = (now + timedelta(seconds=remaining)) if is_running else (
                end_dt or start_dt + timedelta(seconds=time_limit_seconds + total_paused_seconds))

        return {
            "start_time": start_dt,
            "end_time": end_dt if not is_running else None,
            "status": status or None,
            "is_running": is_running,
            "wall_seconds": wall_seconds,
            "total_paused_seconds": total_paused_seconds,
            "active_seconds": active_seconds,
            "active_hms": self._format_hms(active_seconds),
            "time_limit_seconds": time_limit_seconds,
            "time_remaining_seconds": time_remaining_seconds,
            "estimated_end_time": estimated_end_time,
            "reference_end_time": ref_end_dt,
        }

    def _extract_hourly_rate(self, session_data: Dict[str, Any]) -> float:
        # Direct hourly rate keys
        candidates = [
            "cost_per_hour", "hourly_cost", "hourly_rate", "price_per_hour", "per_hour_cost",
            "rate_usd_per_hour", "hourlyUsd", "hourlyUSD"
        ]
        for k in candidates:
            v = session_data.get(k)
            if isinstance(v, (int, float)):
                return float(v)
        # Nested pricing dict
        pricing = session_data.get("pricing") or session_data.get("cost") or {}
        if isinstance(pricing, dict):
            for k in candidates + ["hour", "per_hour"]:
                v = pricing.get(k)
                if isinstance(v, (int, float)):
                    return float(v)
            # cents per hour
            cents = pricing.get(
                "cents_per_hour") or pricing.get("hourly_cents")
            if isinstance(cents, (int, float)):
                return float(cents) / 100.0
        # Minute rate
        per_min = session_data.get(
            "cost_per_minute") or session_data.get("per_minute_cost")
        if isinstance(per_min, (int, float)):
            return float(per_min) * 60.0
        # Second rate
        per_sec = session_data.get(
            "cost_per_second") or session_data.get("per_second_cost")
        if isinstance(per_sec, (int, float)):
            return float(per_sec) * 3600.0
        # Cents per hour direct
        cents_per_hour = session_data.get(
            "cents_per_hour") or session_data.get("hourly_cents")
        if isinstance(cents_per_hour, (int, float)):
            return float(cents_per_hour) / 100.0
        return 0.0

    def _extract_base_cost(self, session_data: Dict[str, Any]) -> float:
        base_keys = ["base_cost", "fixed_cost", "setup_cost",
                     "initial_cost", "baseCost", "fixedCost"]
        for k in base_keys:
            v = session_data.get(k)
            if isinstance(v, (int, float)):
                return float(v)
        return 0.0

    def _extract_cost_limit(self, session_data: Dict[str, Any], cost_limit: Optional[float]) -> Optional[float]:
        if isinstance(cost_limit, (int, float)):
            return float(cost_limit)
        v = self._get_first(
            session_data,
            ["cost_limit", "budget", "budget_usd", "spend_limit_usd",
                "costLimit", "budgetUsd", "budgetUSD"],
            None,
        )
        if isinstance(v, (int, float)):
            return float(v)
        return self.default_cost_limit

    def calculate_cost_predictions(self, session_data: Dict[str, Any], time_data: Dict[str, Any], cost_limit: Optional[float] = None) -> Dict[str, Any]:
        """Calculate cost-related predictions.
        Args:
            session_data: Dictionary containing session cost information
            time_data: Time data from calculate_time_data
            cost_limit: Optional cost limit (defaults to 100.0)
        Returns:
            Dictionary with cost predictions
        """
        hourly_rate = max(0.0, float(self._extract_hourly_rate(session_data)))
        per_second_rate = hourly_rate / 3600.0

        active_seconds = int(max(0, int(time_data.get("active_seconds") or 0)))
        is_running = bool(time_data.get("is_running"))
        base_cost = self._extract_base_cost(session_data)

        # If an explicit accrued cost exists, prefer the larger to avoid undercounting
        accrued_candidates = [
            "accrued_cost", "cost_so_far", "total_cost", "spent_usd", "spend_usd", "cost"
        ]
        accrued_explicit = None
        for k in accrued_candidates:
            v = session_data.get(k)
            if isinstance(v, (int, float)):
                accrued_explicit = float(v) if accrued_explicit is None else max(
                    accrued_explicit, float(v))
        accrued_cost = base_cost + (per_second_rate * active_seconds)
        if accrued_explicit is not None:
            accrued_cost = max(accrued_cost, accrued_explicit)

        # Normalize to 4 decimal places for cents precision safety
        accrued_cost = round(accrued_cost, 4)

        limit = self._extract_cost_limit(session_data, cost_limit)
        remaining_budget = None if limit is None else round(
            max(0.0, float(limit) - accrued_cost), 4)

        if is_running and per_second_rate > 0 and remaining_budget is not None:
            time_until_limit_seconds = int(
                max(0.0, remaining_budget / per_second_rate))
        else:
            time_until_limit_seconds = None

        projected_total_cost_1h = round(
            accrued_cost + hourly_rate, 4) if is_running else accrued_cost
        projected_total_cost_8h = round(
            accrued_cost + 8 * hourly_rate, 4) if is_running else accrued_cost
        projected_total_cost_24h = round(
            accrued_cost + 24 * hourly_rate, 4) if is_running else accrued_cost

        return {
            "cost_per_hour": hourly_rate,
            "cost_per_minute": hourly_rate / 60.0,
            "cost_per_second": per_second_rate,
            "base_cost": base_cost,
            "accrued_cost": accrued_cost,
            "cost_limit": limit,
            "remaining_budget": remaining_budget,
            "time_until_limit_seconds": time_until_limit_seconds,
            "projected_total_cost_1h": projected_total_cost_1h,
            "projected_total_cost_8h": projected_total_cost_8h,
            "projected_total_cost_24h": projected_total_cost_24h,
            "over_budget": (remaining_budget is not None and remaining_budget <= 0.0),
        }
