import time
from task_storage import TaskStorage

class AgentLogger:

    def __init__(self, run_id: str, task_id: str=None):
        self.run_id = run_id
        self.task_id = task_id or run_id
        self.verbose = False
        self.task_storage = TaskStorage()
        self._setup_log_document()

    def load_log_document(self) -> dict:
        """
        Load the log document - returns the auto-persisting log dict.
        """
        return dict(self.log_document)

    def log_message(self, message: dict):
        """
        Update the log document with a new message - auto-saves to database!
        """
        self.log_document['progress'].append(message)
        self.log_document['last_updated'] = time.strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f'Task: {self.task_id} | Run: {self.run_id} | Message: {message}'
        logger.info(log_entry)

    def _setup_log_document(self):
        """
        Setup the auto-persisting log document.
        """
        existing_log = self.task_storage.load_log(self.run_id, 'agent_logger')
        if existing_log:
            self.log_document = self.task_storage.create_log_persistent(self.task_id, self.run_id, 'agent_logger', existing_log)
        else:
            initial_log_data = {'task_id': self.task_id, 'run_id': self.run_id, 'last_updated': time.strftime('%Y-%m-%d %H:%M:%S'), 'progress': []}
            self.log_document = self.task_storage.create_log_persistent(self.task_id, self.run_id, 'agent_logger', initial_log_data)
            self.task_storage.add_run_id_to_task(self.task_id, self.run_id)
            logger.info(f'Initialized logger for Task: {self.task_id} | Run: {self.run_id}')