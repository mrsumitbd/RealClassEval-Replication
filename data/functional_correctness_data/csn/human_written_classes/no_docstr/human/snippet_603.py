class QueueDetails:

    def __init__(self, name, service):
        self.name = name
        self.service = service

    def __str__(self):
        return 'QueueDetails({0.name})'.format(self)