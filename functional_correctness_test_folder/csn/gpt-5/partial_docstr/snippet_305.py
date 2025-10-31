class QuotaBase:
    '''Quota base functionality.'''

    def _iter_resources(self):
        resources = []
        if hasattr(self, 'resources'):
            resources = self.resources
            if callable(resources):
                resources = resources()
        elif hasattr(self, 'get_resources') and callable(getattr(self, 'get_resources')):
            resources = self.get_resources()
        return resources or []

    def _normalize_resource(self, item):
        if isinstance(item, dict):
            rtype = item.get('type', item.get('resource_type'))
            usage = item.get('usage', 0)
            limit = item.get('limit')
        elif isinstance(item, (list, tuple)) and len(item) >= 3:
            rtype, usage, limit = item[0], item[1], item[2]
        else:
            raise ValueError('Unsupported resource item format')
        return rtype, float(usage or 0), (None if limit is None else float(limit))

    def _get_health_status(self, usage, limit):
        if limit in (None, 0):
            return 'unknown'
        ratio = usage / limit
        if ratio < 0.8:
            return 'ok'
        if ratio < 1.0:
            return 'warning'
        return 'critical'

    def _get_quota_by_type(self, resource_type):
        '''Aggregate quota usage by resource type.'''
        total_usage = 0.0
        total_limit = 0.0
        any_limit = False

        for item in self._iter_resources():
            rtype, usage, limit = self._normalize_resource(item)
            if rtype != resource_type:
                continue
            total_usage += usage
            if limit is not None:
                total_limit += limit
                any_limit = True

        limit_val = total_limit if any_limit else None
        remaining = (
            limit_val - total_usage) if limit_val is not None else None
        percent_used = (
            total_usage / limit_val) if (limit_val not in (None, 0)) else None
        status = self._get_health_status(total_usage, limit_val)

        return {
            'type': resource_type,
            'usage': total_usage,
            'limit': limit_val,
            'remaining': remaining,
            'percent_used': percent_used,
            'status': status,
        }

    def get_quota_usage(self):
        types = set()
        for item in self._iter_resources():
            rtype, _, _ = self._normalize_resource(item)
            types.add(rtype)
        return {t: self._get_quota_by_type(t) for t in sorted(types)}
