
class QuotaBase:
    '''Quota base functionality.'''

    def _get_quota_by_type(self, resource_type):
        '''Aggregate quota usage by resource type.'''
        quota_by_type = {}
        for resource in self.resources:
            if resource.type == resource_type:
                if resource_type in quota_by_type:
                    quota_by_type[resource_type] += resource.usage
                else:
                    quota_by_type[resource_type] = resource.usage
        return quota_by_type

    def _get_health_status(self, usage, limit):
        '''Calculate quota health status.'''
        if usage >= limit:
            return 'CRITICAL'
        elif usage >= 0.9 * limit:
            return 'WARNING'
        else:
            return 'OK'

    def get_quota_usage(self):
        '''Get quota usage information.'''
        quota_usage = {}
        for resource_type in self.resource_types:
            usage = self._get_quota_by_type(resource_type)
            quota_usage[resource_type] = {
                'usage': usage,
                'limit': self.limits[resource_type],
                'health_status': self._get_health_status(usage, self.limits[resource_type])
            }
        return quota_usage
