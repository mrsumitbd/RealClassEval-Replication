
class QuotaBase:

    def _get_quota_by_type(self, resource_type):
        # Assuming a dictionary that maps resource types to their respective quotas
        quotas = {
            'storage': {'limit': 100, 'usage': 50},
            'compute': {'limit': 1000, 'usage': 500},
            'network': {'limit': 500, 'usage': 200}
        }

        quota = quotas.get(resource_type)
        if quota is None:
            raise ValueError(f"Unknown resource type: {resource_type}")

        usage = quota['usage']
        limit = quota['limit']

        def _get_health_status(usage, limit):
            if limit == 0:
                return 'N/A'
            elif usage / limit < 0.5:
                return 'Healthy'
            elif usage / limit < 0.8:
                return 'Warning'
            else:
                return 'Critical'

        health_status = _get_health_status(usage, limit)
        return {'usage': usage, 'limit': limit, 'health_status': health_status}

    def get_quota_usage(self):
        resource_types = ['storage', 'compute', 'network']
        quota_usages = {}

        for resource_type in resource_types:
            quota_usage = self._get_quota_by_type(resource_type)
            quota_usages[resource_type] = quota_usage

        return quota_usages


# Example usage:
if __name__ == "__main__":
    quota_base = QuotaBase()
    quota_usages = quota_base.get_quota_usage()
    for resource_type, quota_usage in quota_usages.items():
        print(f"Resource Type: {resource_type}")
        print(f"Usage: {quota_usage['usage']}")
        print(f"Limit: {quota_usage['limit']}")
        print(f"Health Status: {quota_usage['health_status']}")
        print("-" * 20)
