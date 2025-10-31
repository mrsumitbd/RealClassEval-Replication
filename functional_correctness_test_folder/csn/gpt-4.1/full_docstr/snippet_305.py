
class QuotaBase:
    '''Quota base functionality.'''

    def _get_quota_by_type(self, resource_type):
        '''Aggregate quota usage by resource type.'''
        # This is a stub. In a real implementation, this would query a data source.
        # For demonstration, let's assume self.quotas is a dict like:
        # {'cpu': {'used': 5, 'limit': 10}, 'ram': {'used': 8, 'limit': 16}}
        if not hasattr(self, 'quotas'):
            self.quotas = {}
        return self.quotas.get(resource_type, {'used': 0, 'limit': 0})

    @staticmethod
    def _get_health_status(usage, limit):
        '''Calculate quota health status.'''
        if limit == 0:
            return 'unlimited'
        ratio = usage / limit
        if ratio < 0.7:
            return 'healthy'
        elif ratio < 0.9:
            return 'warning'
        else:
            return 'critical'

    def get_quota_usage(self):
        '''Get quota usage information.'''
        if not hasattr(self, 'quotas'):
            self.quotas = {}
        usage_info = {}
        for resource_type, data in self.quotas.items():
            used = data.get('used', 0)
            limit = data.get('limit', 0)
            status = self._get_health_status(used, limit)
            usage_info[resource_type] = {
                'used': used,
                'limit': limit,
                'status': status
            }
        return usage_info
