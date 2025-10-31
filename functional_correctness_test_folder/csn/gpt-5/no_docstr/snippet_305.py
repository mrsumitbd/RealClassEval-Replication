class QuotaBase:
    HEALTH_WARNING_THRESHOLD = 0.7
    HEALTH_CRITICAL_THRESHOLD = 0.9

    def _get_quota_by_type(self, resource_type):
        quotas = self.get_quota_usage()
        return quotas.get(resource_type)

    def _get_health_status(self, usage, limit):
        try:
            usage = 0 if usage is None else float(usage)
        except (TypeError, ValueError):
            return "unknown"

        if limit is None:
            return "unknown"

        try:
            limit = float(limit)
        except (TypeError, ValueError):
            return "unknown"

        if limit < 0 or usage < 0:
            return "unknown"

        if limit == 0:
            return "over" if usage > 0 else "blocked"

        if usage > limit:
            return "over"

        ratio = usage / limit
        if ratio >= self.HEALTH_CRITICAL_THRESHOLD:
            return "critical"
        if ratio >= self.HEALTH_WARNING_THRESHOLD:
            return "warning"
        return "healthy"

    def get_quota_usage(self):
        raw = getattr(self, "quotas", None)
        if callable(raw):
            raw = raw()
        if raw is None:
            return {}

        result = {}
        if isinstance(raw, dict):
            for rtype, val in raw.items():
                used = None
                limit = None
                if isinstance(val, dict):
                    used = val.get("used", val.get("usage", 0))
                    limit = val.get("limit")
                elif isinstance(val, (list, tuple)) and len(val) >= 2:
                    used, limit = val[0], val[1]
                elif isinstance(val, (int, float)):
                    limit = val
                    used = 0
                else:
                    continue

                try:
                    used_f = float(0 if used is None else used)
                except (TypeError, ValueError):
                    used_f = None
                try:
                    limit_f = None if limit is None else float(limit)
                except (TypeError, ValueError):
                    limit_f = None

                health = self._get_health_status(used_f, limit_f)

                if limit_f in (None,):
                    remaining = None
                    percent_used = None
                else:
                    remaining = None if used_f is None else max(
                        limit_f - used_f, 0)
                    percent_used = None if used_f is None or limit_f == 0 else min(
                        used_f / limit_f, 1.0)

                result[rtype] = {
                    "used": used_f if used_f is not None else 0.0,
                    "limit": limit_f,
                    "remaining": remaining,
                    "percent_used": percent_used,
                    "health": health,
                }
        return result
