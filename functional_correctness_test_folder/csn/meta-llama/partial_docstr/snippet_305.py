
class QuotaBase:
    '''Quota base functionality.'''

    def __init__(self, quota_data):
        """
        Initialize the QuotaBase class.

        :param quota_data: A dictionary containing quota data.
        """
        self.quota_data = quota_data

    def _get_quota_by_type(self, resource_type):
        '''Aggregate quota usage by resource type.'''
        usage = sum(item.get('used', 0)
                    for item in self.quota_data if item.get('type') == resource_type)
        limit = sum(item.get('limit', 0)
                    for item in self.quota_data if item.get('type') == resource_type)
        return usage, limit

    def _get_health_status(self, usage, limit):
        '''Determine the health status based on quota usage.'''
        if limit == 0:
            return 'Unknown'
        elif usage / limit >= 0.9:
            return 'Critical'
        elif usage / limit >= 0.7:
            return 'Warning'
        else:
            return 'Healthy'

    def get_quota_usage(self):
        '''Get quota usage for all resource types.'''
        quota_usage = {}
        resource_types = set(item.get('type') for item in self.quota_data)
        for resource_type in resource_types:
            usage, limit = self._get_quota_by_type(resource_type)
            health_status = self._get_health_status(usage, limit)
            quota_usage[resource_type] = {
                'usage': usage,
                'limit': limit,
                'health_status': health_status
            }
        return quota_usage


# Example usage:
if __name__ == "__main__":
    quota_data = [
        {'type': 'storage', 'used': 100, 'limit': 1000},
        {'type': 'storage', 'used': 200, 'limit': 1000},
        {'type': 'compute', 'used': 500, 'limit': 1000},
        {'type': 'compute', 'used': 300, 'limit': 1000},
    ]

    quota_base = QuotaBase(quota_data)
    quota_usage = quota_base.get_quota_usage()
    for resource_type, usage_data in quota_usage.items():
        print(f"Resource Type: {resource_type}")
        print(f"Usage: {usage_data['usage']}")
        print(f"Limit: {usage_data['limit']}")
        print(f"Health Status: {usage_data['health_status']}")
        print("------------------------")
