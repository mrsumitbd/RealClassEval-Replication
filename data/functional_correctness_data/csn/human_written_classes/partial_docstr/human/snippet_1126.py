class JobResult:
    """Class to store the result of a Perceval job.

    It stores the summary of a Perceval job and other useful data
    such as the task and job identifiers, the backend and the
    category of the items generated.

    :param job_id: job identifier
    :param job_number: human readable identifier for this job
    :param task_id: identifier of the task linked to this job
    :param backend: backend used to fetch the items
    :param category: category of the fetched items
    """

    def __init__(self, job_id, job_number, task_id, backend, category):
        self.job_id = job_id
        self.job_number = job_number
        self.task_id = task_id
        self.backend = backend
        self.category = category
        self.summary = None

    def to_dict(self):
        """Convert object to a dict"""
        result = {'job_id': self.job_id, 'job_number': self.job_number, 'task_id': self.task_id}
        if self.summary:
            result['fetched'] = self.summary.fetched
            result['skipped'] = self.summary.skipped
            result['min_updated_on'] = self.summary.min_updated_on.timestamp()
            result['max_updated_on'] = self.summary.max_updated_on.timestamp()
            result['last_updated_on'] = self.summary.last_updated_on.timestamp()
            result['last_uuid'] = self.summary.last_uuid
            result['min_offset'] = self.summary.min_offset
            result['max_offset'] = self.summary.max_offset
            result['last_offset'] = self.summary.last_offset
            result['extras'] = self.summary.extras
        return result