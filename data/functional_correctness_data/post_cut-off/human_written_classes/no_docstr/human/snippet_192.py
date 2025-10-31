from queue import Queue
import time
from strands_tools.use_llm import use_llm
import uuid
from typing import Any, Dict, List
from threading import Lock

class AgentNode:

    def __init__(self, node_id: str, role: str, system_prompt: str):
        self.id = node_id
        self.role = role
        self.system_prompt = system_prompt
        self.neighbors = []
        self.input_queue = Queue(maxsize=MAX_QUEUE_SIZE)
        self.is_running = True
        self.thread = None
        self.last_process_time = 0
        self.lock = Lock()

    def add_neighbor(self, neighbor):
        with self.lock:
            if neighbor not in self.neighbors:
                self.neighbors.append(neighbor)

    def process_messages(self, tool_context: Dict[str, Any], channel: str):
        while self.is_running:
            try:
                current_time = time.time()
                if current_time - self.last_process_time < MESSAGE_PROCESSING_DELAY:
                    time.sleep(MESSAGE_PROCESSING_DELAY)
                if not self.input_queue.empty():
                    message = self.input_queue.get_nowait()
                    self.last_process_time = current_time
                    try:
                        result = use_llm({'toolUseId': str(uuid.uuid4()), 'input': {'system_prompt': self.system_prompt, 'prompt': message['content']}}, **tool_context)
                        if result.get('status') == 'success':
                            response_content = ''
                            for content in result.get('content', []):
                                if content.get('text'):
                                    response_content += content['text'] + '\n'
                            broadcast_message = {'from': self.id, 'content': response_content.strip()}
                            for neighbor in self.neighbors:
                                if not neighbor.input_queue.full():
                                    neighbor.input_queue.put_nowait(broadcast_message)
                                else:
                                    logger.warning(f'Message queue full for neighbor {neighbor.id}')
                    except Exception as e:
                        logger.error(f'Error processing message in node {self.id}: {str(e)}')
                else:
                    time.sleep(MESSAGE_PROCESSING_DELAY)
            except Exception as e:
                logger.error(f'Error in message processing loop for node {self.id}: {str(e)}')
                time.sleep(MESSAGE_PROCESSING_DELAY)