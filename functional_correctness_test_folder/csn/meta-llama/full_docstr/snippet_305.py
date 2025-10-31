
class QuotaBase:
    '''Quota base functionality.'''

    def __init__(self, quota_data):
        """
        Initialize QuotaBase instance.

        :param quota_data: A dictionary containing quota information.
        """
        self.quota_data = quota_data

    def _get_quota_by_type(self, resource_type):
        '''Aggregate quota usage by resource type.'''
        usage = sum(item['used']
                    for item in self.quota_data if item['type'] == resource_type)
        limit = sum(item['limit']
                    for item in self.quota_data if item['type'] == resource_type)
        return usage, limit

    def _get_health_status(self, usage, limit):
        '''Calculate quota health status.'''
        if limit == 0:
            return 'N/A'
        elif usage / limit < 0.8:
            return 'Healthy'
        elif usage / limit < 1.0:
            return 'Warning'
        else:
            return 'Critical'

    def get_quota_usage(self):
        '''Get quota usage information.'''
        quota_usage_info = {}
        resource_types = set(item['type'] for item in self.quota_data)

        for resource_type in resource_types:
            usage, limit = self._get_quota_by_type(resource_type)
            health_status = self._get_health_status(usage, limit)
            quota_usage_info[resource_type] = {
                'usage': usage,
                'limit': limit,
                'health_status': health_status
            }

        return quota_usage_info


# Example usage:
if __name__ == "__main__":
    quota_data = [
        {'type': 'storage', 'used': 100, 'limit': 1000},
        {'type': 'storage', 'used': 200, 'limit': 1000},
        {'type': 'compute', 'used': 500, 'limit': 1000},
        {'type': 'compute', 'used': 600, 'limit': 1000},
    ]

    quota_base = QuotaBase(quota_data)
    quota_usage_info = quota_base.get_quota_usage()
    for resource_type, info in quota_usage_info.items():
        print(f"Resource Type: {resource_type}")
        print(f"Usage: {info['usage']}")
        print(f"Limit: {info['limit']}")
        print(f"Health Status: {info['health_status']}")
        print("-" * 20)
