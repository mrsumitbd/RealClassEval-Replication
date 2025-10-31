from datetime import datetime

class History:

    def __init__(self, id, event, **kwargs):
        self.id = id
        self.event = event
        self.severity = kwargs.get('severity', None)
        self.status = kwargs.get('status', None)
        self.value = kwargs.get('value', None)
        self.text = kwargs.get('text', None)
        self.change_type = kwargs.get('change_type', kwargs.get('type', None)) or ''
        self.update_time = kwargs.get('update_time', None) or datetime.utcnow()
        self.user = kwargs.get('user', None)

    def __repr__(self):
        return 'History(id={!r}, event={!r}, severity={!r}, status={!r}, type={!r})'.format(self.id, self.event, self.severity, self.status, self.change_type)