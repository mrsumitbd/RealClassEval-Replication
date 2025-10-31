from typing import List, Optional
import time

class MessageProcessor:
    """Message processing for Amp integration"""

    def __init__(self, wrapper: 'AmpWrapper'):
        self.wrapper = wrapper
        self.last_message_id = None
        self.last_message_time = None
        self.web_ui_messages = set()
        self.pending_input_message_id = None
        self.in_thinking = False
        self.thinking_buffer = ''

    def process_user_message_sync(self, content: str, from_web: bool) -> None:
        """Process a user message"""
        if from_web:
            self.web_ui_messages.add(content)
        elif content not in self.web_ui_messages:
            self.wrapper.log(f'[INFO] Sending user message to Omnara: {content[:50]}...')
            if self.wrapper.agent_instance_id and self.wrapper.omnara_client_sync:
                self.wrapper.omnara_client_sync.send_user_message(agent_instance_id=self.wrapper.agent_instance_id, content=content)
        else:
            self.web_ui_messages.discard(content)
        self.last_message_time = time.time()
        self.pending_input_message_id = None

    def process_assistant_message_sync(self, content: str) -> None:
        """Process an assistant message from Amp"""
        if not self.wrapper.omnara_client_sync:
            return
        sanitized_content = ''.join((char if ord(char) >= 32 or char in '\n\r\t' else '' for char in content.replace('\x00', '')))
        git_diff = self.wrapper.get_git_diff()
        if git_diff:
            git_diff = ''.join((char if ord(char) >= 32 or char in '\n\r\t' else '' for char in git_diff.replace('\x00', '')))
        self.wrapper.log(f'[INFO] Sending assistant message to Omnara API: {sanitized_content[:100]}...')
        self.wrapper.log(f'[DEBUG] Agent instance ID: {self.wrapper.agent_instance_id}')
        response = self.wrapper.omnara_client_sync.send_message(content=sanitized_content, agent_type='Amp', agent_instance_id=self.wrapper.agent_instance_id, requires_user_input=False, git_diff=git_diff)
        self.wrapper.log(f'[INFO] Message sent successfully, response ID: {response.message_id}')
        if not self.wrapper.agent_instance_id:
            self.wrapper.agent_instance_id = response.agent_instance_id
            self.wrapper.log(f'[INFO] Stored agent instance ID: {self.wrapper.agent_instance_id}')
        self.last_message_id = response.message_id
        self.last_message_time = time.time()
        if response.queued_user_messages:
            self.wrapper.log(f'[INFO] Got {len(response.queued_user_messages)} queued user messages')
            concatenated = '\n'.join(response.queued_user_messages)
            self.web_ui_messages.add(concatenated)
            self.wrapper.input_queue.append(concatenated)

    def should_request_input(self) -> Optional[str]:
        """Check if we should request input from web UI"""
        if self.last_message_id and self.last_message_id != self.pending_input_message_id and self.wrapper.is_amp_idle():
            return self.last_message_id
        return None

    def mark_input_requested(self, message_id: str) -> None:
        """Mark that input has been requested"""
        self.pending_input_message_id = message_id