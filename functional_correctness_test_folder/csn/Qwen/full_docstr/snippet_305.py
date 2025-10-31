
class QuotaBase:
    '''Quota base functionality.'''

    def _get_quota_by_type(self, resource_type):
        '''Aggregate quota usage by resource type.'''
        # Example implementation
        # This should be replaced with actual logic to aggregate quota usage
        return {
            'used': 0,
            'limit': 100
        }

    def _get_health_status(self, usage, limit):
        '''Calculate quota health status.'''
        # Example implementation
        # This should be replaced with actual logic to determine health status
        if usage < limit:
            return 'HEALTHY'
        elif usage == limit:
            return 'WARNING'
        else:
            return 'CRITICAL'

    def get_quota_usage(self):
        '''Get quota usage information.'''
        # Example implementation
        # This should be replaced with actual logic to gather quota usage information
        resource_types = ['cpu', 'memory', 'storage']
        quota_usage = {}
        for resource_type in resource_types:
            usage_info = self._get_quota_by_type(resource_type)
            usage_info['health'] = self._get_health_status(
                usage_info['used'], usage_info['limit'])
            quota_usage[resource_type] = usage_info
        return quota_usage
