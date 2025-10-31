class QuotaBase:
    '''Quota base functionality.'''

    def __init__(self, quota_data=None):
        """
        Initialize the QuotaBase with optional quota data.

        :param quota_data: Iterable of dicts with keys:
                           'resource_type', 'usage', 'limit'.
        """
        self.quota_data = list(quota_data or [])

    def _get_quota_by_type(self, resource_type):
        '''Aggregate quota usage by resource type.'''
        filtered = [q for q in self.quota_data if q.get(
            'resource_type') == resource_type]
        total_usage = sum(q.get('usage', 0) for q in filtered)
        total_limit = sum(q.get('limit', 0) for q in filtered)
        return {'resource_type': resource_type, 'usage': total_usage, 'limit': total_limit}

    def _get_health_status(self, usage, limit):
        '''Determine health status based on usage and limit.'''
        if limit == 0:
            return 'unknown'
        percent = usage / limit
        if percent < 0.5:
            return 'healthy'
        elif percent < 0.8:
            return 'warning'
        else:
            return 'critical'

    def get_quota_usage(self):
        '''Return aggregated quota usage for all resource types.'''
        # Determine unique resource types
        resource_types = {q.get('resource_type') for q in self.quota_data}
        result = []
        for rt in resource_types:
            quota = self._get_quota_by_type(rt)
            status = self._get_health_status(quota['usage'], quota['limit'])
            quota['status'] = status
            result.append(quota)
        return result
