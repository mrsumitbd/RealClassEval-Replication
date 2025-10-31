
class QuotaBase:

    def _get_quota_by_type(self, resource_type):
        pass

    def _get_health_status(self, usage, limit):
        pass

    def get_quota_usage(self):
        pass
