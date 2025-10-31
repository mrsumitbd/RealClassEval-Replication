
class QuotaBase:
    def __init__(self, quota_data=None):
        """
        Initialize the QuotaBase with optional quota data.

        :param quota_data: A dictionary mapping resource types to a dict
                           containing 'usage' and 'limit' keys.
        """
        self.quota_data = quota_data or {}

    def _get_quota_by_type(self, resource_type):
        """
        Retrieve the quota information for a specific resource type.

        :param resource_type: The type of resource to look up.
        :return: A dictionary with 'usage' and 'limit' keys.
        """
        return self.quota_data.get(resource_type, {"usage": 0, "limit": 0})

    def _get_health_status(self, usage, limit):
        """
        Determine the health status based on usage and limit.

        :param usage: Current usage value.
        :param limit: Maximum allowed value.
        :return: A string representing the health status ('green', 'yellow', 'red', or 'unknown').
        """
        if limit == 0:
            return "unknown"
        usage_ratio = usage / limit
        if usage_ratio < 0.5:
            return "green"
        if usage_ratio < 0.8:
            return "yellow"
        return "red"

    def get_quota_usage(self):
        """
        Compile a comprehensive report of quota usage for all resource types.

        :return: A dictionary mapping each resource type to its usage, limit, and health status.
        """
        report = {}
        for resource_type, data in self.quota_data.items():
            usage = data.get("usage", 0)
            limit = data.get("limit", 0)
            status = self._get_health_status(usage, limit)
            report[resource_type] = {
                "usage": usage,
                "limit": limit,
                "status": status,
            }
        return report
