class QuotaBase:
    """Quota base functionality."""

    def _get_quota_by_type(self, resource_type):
        """Aggregate quota usage by resource type."""

        def _get_health_status(usage, limit):
            """Calculate quota health status."""
            health = QuotaHealth.healthy
            if limit:
                percentage = usage / limit * 100
                if percentage >= 80:
                    if percentage >= 100:
                        health = QuotaHealth.critical
                    else:
                        health = QuotaHealth.warning
            return health.name
        quota_usage = 0
        quota_limit = 0
        unit = None
        for resource in self.resources:
            if resource.resource.type_ == resource_type:
                if unit and unit != resource.resource.unit:
                    raise Exception('Error while calculating quota usage. Not all resources of resource type {} use the same units.'.format(resource_type))
                unit = resource.resource.unit
                quota_usage += resource.quota_used
                if hasattr(resource, 'quota_limit'):
                    quota_limit += resource.quota_limit
        usage_dict = {'usage': {'raw': quota_usage, 'human_readable': ResourceUnit.human_readable_unit(unit, quota_usage)}}
        if quota_limit:
            usage_dict['limit'] = {'raw': quota_limit, 'human_readable': ResourceUnit.human_readable_unit(unit, quota_limit)}
            usage_dict['health'] = _get_health_status(quota_usage, quota_limit)
        return usage_dict

    def get_quota_usage(self):
        """Get quota usage information."""
        used_resource_types = set((res.resource.type_ for res in self.resources))
        return {resource_type.name: self._get_quota_by_type(resource_type) for resource_type in used_resource_types}