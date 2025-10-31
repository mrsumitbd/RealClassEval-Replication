from datetime import datetime, timedelta
from any_agent.tracing.agent_trace import AgentMessage, AgentTrace

class ContextData:
    """Data stored for each task."""

    def __init__(self, task_id: str):
        """Initialize task data.

        Args:
            task_id: Unique identifier for the task

        """
        self.task_id = task_id
        self.conversation_history: list[AgentMessage] = []
        self.last_activity = datetime.now()
        self.created_at = datetime.now()

    def update_activity(self) -> None:
        """Update the last activity timestamp."""
        self.last_activity = datetime.now()

    def is_expired(self, timeout_minutes: int) -> bool:
        """Check if the task has expired.

        Args:
            timeout_minutes: Timeout in minutes

        Returns:
            True if task is expired, False otherwise

        """
        expiration_time = self.last_activity + timedelta(minutes=timeout_minutes)
        return datetime.now() > expiration_time