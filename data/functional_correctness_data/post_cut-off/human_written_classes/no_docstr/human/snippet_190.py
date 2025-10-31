from typing import Any, Dict, List
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

class AgentGraph:

    def __init__(self, graph_id: str, topology_type: str, tool_context: Dict[str, Any]):
        self.graph_id = graph_id
        self.topology_type = topology_type
        self.nodes = {}
        self.tool_context = tool_context
        self.channel = f'agent_graph_{graph_id}'
        self.thread_pool = ThreadPoolExecutor(max_workers=MAX_THREADS)
        self.lock = Lock()

    def add_node(self, node_id: str, role: str, system_prompt: str):
        with self.lock:
            node = AgentNode(node_id, role, system_prompt)
            self.nodes[node_id] = node
            return node

    def add_edge(self, from_id: str, to_id: str):
        with self.lock:
            if from_id in self.nodes and to_id in self.nodes:
                self.nodes[from_id].add_neighbor(self.nodes[to_id])
                if self.topology_type == 'mesh':
                    self.nodes[to_id].add_neighbor(self.nodes[from_id])

    def start(self):
        try:
            with self.lock:
                for node in self.nodes.values():
                    node.thread = self.thread_pool.submit(node.process_messages, self.tool_context, self.channel)
        except Exception as e:
            logger.error(f'Error starting graph {self.graph_id}: {str(e)}')
            raise

    def stop(self):
        try:
            with self.lock:
                for node in self.nodes.values():
                    node.is_running = False
            self.thread_pool.shutdown(wait=True)
        except Exception as e:
            logger.error(f'Error stopping graph {self.graph_id}: {str(e)}')
            raise

    def send_message(self, target_id: str, message: str):
        try:
            with self.lock:
                if target_id in self.nodes:
                    if not self.nodes[target_id].input_queue.full():
                        self.nodes[target_id].input_queue.put_nowait({'content': message})
                        return True
                    else:
                        logger.warning(f'Message queue full for node {target_id}')
                        return False
                return False
        except Exception as e:
            logger.error(f'Error sending message to node {target_id}: {str(e)}')
            return False

    def get_status(self):
        with self.lock:
            status = {'graph_id': self.graph_id, 'topology': self.topology_type, 'nodes': [{'id': node.id, 'role': node.role, 'neighbors': [n.id for n in node.neighbors], 'queue_size': node.input_queue.qsize()} for node in self.nodes.values()]}
            return status