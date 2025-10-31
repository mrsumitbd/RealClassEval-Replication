class QuotaBase:
    '''Quota base functionality.'''

    def _get_quota_by_type(self, resource_type):
        '''Aggregate quota usage by resource type.'''
        total_usage = 0
        total_limit = 0
        has_limit = False

        resources = []
        if hasattr(self, "resources"):
            resources = getattr(self, "resources") or []
        elif hasattr(self, "get_resources") and callable(getattr(self, "get_resources")):
            resources = getattr(self, "get_resources")() or []

        for res in resources:
            if not isinstance(res, dict):
                continue
            if res.get("type") != resource_type:
                continue
            usage = res.get("usage")
            limit = res.get("limit")

            try:
                usage_val = float(usage) if usage is not None else 0.0
            except (TypeError, ValueError):
                usage_val = 0.0

            if limit is None:
                # If any item has unknown limit, treat overall limit as unknown
                pass
            else:
                try:
                    limit_val = float(limit)
                except (TypeError, ValueError):
                    limit_val = None

                if limit_val is not None:
                    total_limit += max(limit_val, 0.0)
                    has_limit = True

            total_usage += max(usage_val, 0.0)

        limit_value = total_limit if has_limit else None

        if limit_value is None:
            remaining = None
            percentage = None
        else:
            remaining = max(limit_value - total_usage, 0.0)
            percentage = (total_usage / limit_value *
                          100.0) if limit_value > 0 else 0.0

        status = self._get_health_status(total_usage, limit_value)

        return {
            "type": resource_type,
            "usage": total_usage,
            "limit": limit_value,
            "remaining": remaining,
            "percentage": round(percentage, 2) if percentage is not None else None,
            "status": status,
        }

    def _get_health_status(self, usage, limit):
        '''Calculate quota health status.'''
        try:
            usage_val = float(usage) if usage is not None else 0.0
        except (TypeError, ValueError):
            usage_val = 0.0

        if limit is None:
            return "unknown"

        try:
            limit_val = float(limit)
        except (TypeError, ValueError):
            return "unknown"

        if limit_val <= 0:
            return "unknown"

        ratio = usage_val / limit_val

        if ratio >= 0.9:
            return "critical"
        if ratio >= 0.75:
            return "warning"
        return "ok"

    def get_quota_usage(self):
        '''Get quota usage information.'''
        resources = []
        if hasattr(self, "resources"):
            resources = getattr(self, "resources") or []
        elif hasattr(self, "get_resources") and callable(getattr(self, "get_resources")):
            resources = getattr(self, "get_resources")() or []

        types = []
        seen = set()
        for res in resources:
            if not isinstance(res, dict):
                continue
            rtype = res.get("type")
            if rtype is None:
                continue
            if rtype not in seen:
                seen.add(rtype)
                types.append(rtype)

        result = {}
        for t in types:
            result[t] = self._get_quota_by_type(t)

        return result
