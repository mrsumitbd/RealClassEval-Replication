
class QuotaBase:

    def _get_quota_by_type(self, resource_type):
        # Simulate retrieving quota for a given resource type
        quotas = {
            'cpu': {'limit': 10, 'usage': 5},
            'memory': {'limit': 1024, 'usage': 512},
            'storage': {'limit': 10000, 'usage': 5000}
        }
        return quotas.get(resource_type, {'limit': 0, 'usage': 0})

        def _get_health_status(usage, limit):
            # Simulate health status check
            if usage < limit * 0.75:
                return 'healthy'
            elif usage < limit:
                return 'warning'
            else:
                return 'critical'

    def get_quota_usage(self):
        # Example usage of _get_quota_by_type and _get_health_status
        resource_types = ['cpu', 'memory', 'storage']
        results = {}
        for resource_type in resource_types:
            quota_info = self._get_quota_by_type(resource_type)
            health_status = self._get_health_status(
                quota_info['usage'], quota_info['limit'])
            results[resource_type] = {
                'usage': quota_info['usage'],
                'limit': quota_info['limit'],
                'status': health_status
            }
        return results

    def _get_health_status(self, usage, limit):
        # Health status check
        if usage < limit * 0.75:
            return 'healthy'
        elif usage < limit:
            return 'warning'
        else:
            return 'critical'
