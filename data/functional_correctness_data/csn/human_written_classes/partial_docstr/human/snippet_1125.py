import pickle
from grimoirelab_toolkit.datetime import datetime_utcnow
import uuid

class JobEvent:
    """Job activity notification.

    Job events can be used to notify the activity of a job. Usually,
    they will inform whether the job was completed or finished with
    a failure.

    Each event has a type, a unique identifier and the time when it
    was generated (in UTC), the identifier of the job and task that
    produced it and a payload. Depending on the type of event, the
    payload might contain different data.

    :param type: event type
    :param job_id: identifier of the job
    :param task_id: identifier of the task
    :param payload: data of the event
    """

    def __init__(self, type, job_id, task_id, payload):
        self.uuid = str(uuid.uuid4())
        self.timestamp = datetime_utcnow()
        self.type = type
        self.job_id = job_id
        self.task_id = task_id
        self.payload = payload

    def serialize(self):
        return pickle.dumps(self)

    @classmethod
    def deserialize(cls, data):
        return pickle.loads(data)