
class QuotaBase:
    '''Quota base functionality.'''

    def _get_quota_by_type(self, resource_type):
        '''Aggregate quota usage by resource type.'''
        # Simulate fetching quota usage for a given resource type
        # This is a placeholder implementation
        usage_data = {
            'cpu': {'used': 5, 'limit': 10},
            'memory': {'used': 2048, 'limit': 4096},
            'storage': {'used': 100, 'limit': 200}
        }
        return usage_data.get(resource_type, {'used': 0, 'limit': 0})

    def _get_health_status(self, usage, limit):
        if usage < limit:
            return 'HEALTHY'
        elif usage == limit:
            return 'WARNING'
        else:
            return 'CRITICAL'

    def get_quota_usage(self):
        resource_types = ['cpu', 'memory', 'storage']
        quota_usage = {}
        for resource_type in resource_types:
            usage_info = self._get_quota_by_type(resource_type)
            health_status = self._get_health_status(
                usage_info['used'], usage_info['limit'])
            quota_usage[resource_type] = {
                'used': usage_info['used'],
                'limit': usage_info['limit'],
                'status': health_status
            }
        return quota_usage
