
class QuotaBase:
    '''Quota base functionality.'''

    def __init__(self, resources=None):
        """
        Initialize the quota base with an optional list of resources.

        Each resource should be a dictionary containing at least:
            - 'type':   the resource type (string)
            - 'usage':  the current usage (numeric)
            - 'limit':  the quota limit (numeric)
        """
        self.resources = resources or []

    def _get_quota_by_type(self, resource_type):
        '''Aggregate quota usage by resource type.'''
        filtered = [r for r in self.resources if r.get(
            'type') == resource_type]
        total_usage = sum(r.get('usage', 0) for r in filtered)
        total_limit = sum(r.get('limit', 0) for r in filtered)
        return {
            'type': resource_type,
            'usage': total_usage,
            'limit': total_limit
        }

    def _get_health_status(self, usage, limit):
        '''Calculate quota health status.'''
        if limit == 0:
            return 'UNKNOWN'
        ratio = usage / limit
        if ratio < 0.8:
            return 'OK'
        elif ratio < 1.0:
            return 'WARN'
        else:
            return 'CRITICAL'

    def get_quota_usage(self):
        '''Get quota usage information.'''
        types = {r.get('type') for r in self.resources}
        usage_info = []
        for t in types:
            agg = self._get_quota_by_type(t)
            agg['status'] = self._get_health_status(agg['usage'], agg['limit'])
            usage_info.append(agg)
        return usage_info
