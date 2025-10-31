from collections import OrderedDict

class AccountStorage:
    """Storage of the account."""

    def __init__(self, storage_data):
        self.usage = AccountStorageUsage(storage_data.get('storageUsageInfo'), storage_data.get('quotaStatus'))
        self.usages_by_media = OrderedDict()
        for usage_media in storage_data.get('storageUsageByMedia'):
            self.usages_by_media[usage_media['mediaKey']] = AccountStorageUsageForMedia(usage_media)

    def __str__(self):
        return f'{{usage: {self.usage}, usages_by_media: {self.usages_by_media}}}'

    def __repr__(self):
        return f'<{type(self).__name__}: {self}>'