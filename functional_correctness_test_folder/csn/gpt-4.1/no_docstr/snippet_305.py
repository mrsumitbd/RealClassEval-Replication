
class QuotaBase:

    def _get_quota_by_type(self, resource_type):
        """
        Returns a tuple (usage, limit) for the given resource_type.
        This is a stub and should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    def _get_health_status(self, usage, limit):
        """
        Returns a string representing the health status based on usage and limit.
        - 'healthy' if usage < 80% of limit
        - 'warning' if usage >= 80% and < 100% of limit
        - 'critical' if usage >= limit
        """
        if limit == 0:
            return 'critical'
        ratio = usage / limit
        if ratio < 0.8:
            return 'healthy'
        elif ratio < 1.0:
            return 'warning'
        else:
            return 'critical'

    def get_quota_usage(self):
        """
        Returns a dictionary with resource_type as key and a dict as value:
        {
            'usage': usage,
            'limit': limit,
            'status': health_status
        }
        This is a stub and should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses should implement this method.")
