from datetime import datetime
from uuid import uuid4

class UserSession:

    def __init__(self, user_id: str, max_history=10):
        self.user_id = user_id
        self.session_id = str(uuid4())
        self.history = []
        self.created_at = datetime.now()
        self.last_active = datetime.now()
        self.max_history = max_history

    def add_message(self, role: str, content: str):
        self.history.append({'role': role, 'content': content, 'timestamp': datetime.now().isoformat()})
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
        self.last_active = datetime.now()