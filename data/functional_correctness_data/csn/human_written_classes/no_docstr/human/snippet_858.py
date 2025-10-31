class VolumeSnapshot:

    def __init__(self, data, volume):
        self.volume = volume
        self.id = data['id']
        self.status = data['status']
        self.timestamp = data['timestamp']
        self.created_at = data['created_at']

    def delete(self):
        return self.volume.manager.call_api('/storage/%s/snapshots/%s' % (self.volume.id, self.id), type='DELETE')

    def __str__(self):
        return '%s' % self.id

    def __repr__(self):
        return '{}: {}'.format(self.__class__.__name__, self.id)