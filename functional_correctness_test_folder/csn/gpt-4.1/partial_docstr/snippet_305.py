
class QuotaBase:
    '''Quota base functionality.'''

    def __init__(self):
        # Example structure: {resource_type: {'usage': int, 'limit': int}}
        self.quotas = {}

    def _get_quota_by_type(self, resource_type):
        '''Aggregate quota usage by resource type.'''
        quota = self.quotas.get(resource_type, {'usage': 0, 'limit': 0})
        usage = quota.get('usage', 0)
        limit = quota.get('limit', 0)
        status = self._get_health_status(usage, limit)
        return {
            'resource_type': resource_type,
            'usage': usage,
            'limit': limit,
            'status': status
        }

    def _get_health_status(self, usage, limit):
        if limit == 0:
            return 'unlimited'
        ratio = usage / limit
        if ratio < 0.8:
            return 'healthy'
        elif ratio < 1.0:
            return 'warning'
        else:
            return 'exceeded'

    def get_quota_usage(self):
        result = []
        for resource_type in self.quotas:
            result.append(self._get_quota_by_type(resource_type))
        return result
