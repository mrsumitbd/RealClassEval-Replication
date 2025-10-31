import time
from typing import Any, Dict, Optional

class MessageProcessor:
    """Message processing implementation"""

    def __init__(self, wrapper: 'ClaudeWrapperV3'):
        self.wrapper = wrapper
        self.last_message_id = None
        self.last_message_time = None
        self.web_ui_messages = set()
        self.pending_input_message_id = None
        self.last_was_tool_use = False

    def process_user_message_sync(self, content: str, from_web: bool) -> None:
        """Process a user message (sync version for monitor thread)"""
        if from_web:
            self.web_ui_messages.add(content)
        elif content not in self.web_ui_messages:
            self.wrapper.log(f'[INFO] Sending CLI message to Omnara: {content[:50]}...')
            if self.wrapper.agent_instance_id and self.wrapper.omnara_client_sync:
                self.wrapper.omnara_client_sync.send_user_message(agent_instance_id=self.wrapper.agent_instance_id, content=content)
        else:
            self.web_ui_messages.discard(content)
        self.last_message_time = time.time()
        self.pending_input_message_id = None

    def process_assistant_message_sync(self, content: str, tools_used: list[str]) -> None:
        """Process an assistant message (sync version for monitor thread)"""
        if not self.wrapper.agent_instance_id or not self.wrapper.omnara_client_sync:
            return
        with self.wrapper.send_message_lock:
            self.last_was_tool_use = bool(tools_used)
            sanitized_content = ''.join((char if ord(char) >= 32 or char in '\n\r\t' else '' for char in content.replace('\x00', '')))
            git_diff = self.wrapper.git_tracker.get_diff() if self.wrapper.git_tracker else None
            if git_diff:
                git_diff = ''.join((char if ord(char) >= 32 or char in '\n\r\t' else '' for char in git_diff.replace('\x00', '')))
            response = self.wrapper.omnara_client_sync.send_message(content=sanitized_content, agent_type=self.wrapper.name, agent_instance_id=self.wrapper.agent_instance_id, requires_user_input=False, git_diff=git_diff)
            self.last_message_id = response.message_id
            self.last_message_time = time.time()
            self.wrapper.requested_input_messages.clear()
            self.wrapper.pending_permission_options.clear()
            if response.queued_user_messages:
                concatenated = '\n'.join(response.queued_user_messages)
                self.web_ui_messages.add(concatenated)
                self.wrapper.input_queue.append(concatenated)

    def should_request_input(self) -> Optional[str]:
        """Check if we should request input, returns message_id if yes"""
        if self.last_was_tool_use and self.wrapper.is_claude_idle():
            return None
        if self.last_message_id and self.last_message_id != self.pending_input_message_id and self.wrapper.is_claude_idle():
            return self.last_message_id
        return None

    def mark_input_requested(self, message_id: str) -> None:
        """Mark that input has been requested for a message"""
        self.pending_input_message_id = message_id