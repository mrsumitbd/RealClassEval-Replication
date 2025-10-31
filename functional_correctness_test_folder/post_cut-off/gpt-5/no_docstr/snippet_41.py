class HeaderManager:

    def __init__(self) -> None:
        self._allowed_plans = {"free", "pro", "business", "enterprise"}
        self._base_headers = [
            "Accept: application/json",
            "Content-Type: application/json; charset=utf-8",
        ]

    def create_header(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> list[str]:
        if not isinstance(plan, str) or not plan.strip():
            raise ValueError("plan must be a non-empty string")
        if not isinstance(timezone, str) or not timezone.strip():
            raise ValueError("timezone must be a non-empty string")

        plan_norm = plan.strip().lower()
        if plan_norm not in self._allowed_plans:
            raise ValueError(
                f"unsupported plan '{plan}'. Allowed plans: {sorted(self._allowed_plans)}")

        # Validate timezone using zoneinfo (raises if invalid)
        try:
            from zoneinfo import ZoneInfo  # Python 3.9+
            ZoneInfo(timezone.strip())
        except Exception as exc:
            raise ValueError(f"invalid timezone '{timezone}'") from exc

        return [
            *self._base_headers,
            f"X-Plan: {plan_norm}",
            f"X-Timezone: {timezone.strip()}",
        ]
