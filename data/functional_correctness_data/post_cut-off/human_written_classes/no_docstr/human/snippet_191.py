from threading import Lock
from typing import Any, Dict, List

class AgentGraphManager:

    def __init__(self, tool_context: Dict[str, Any]):
        self.graphs = {}
        self.tool_context = tool_context
        self.lock = Lock()

    def create_graph(self, graph_id: str, topology: Dict) -> Dict:
        with self.lock:
            if graph_id in self.graphs:
                return {'status': 'error', 'message': f'Graph {graph_id} already exists'}
            try:
                graph = AgentGraph(graph_id, topology['type'], self.tool_context)
                for node_def in topology['nodes']:
                    graph.add_node(node_def['id'], node_def['role'], node_def['system_prompt'])
                if 'edges' in topology:
                    for edge in topology['edges']:
                        graph.add_edge(edge['from'], edge['to'])
                self.graphs[graph_id] = graph
                graph.start()
                return {'status': 'success', 'message': f'Graph {graph_id} created and started'}
            except Exception as e:
                return {'status': 'error', 'message': f'Error creating graph: {str(e)}'}

    def stop_graph(self, graph_id: str) -> Dict:
        with self.lock:
            if graph_id not in self.graphs:
                return {'status': 'error', 'message': f'Graph {graph_id} not found'}
            try:
                self.graphs[graph_id].stop()
                del self.graphs[graph_id]
                return {'status': 'success', 'message': f'Graph {graph_id} stopped and removed'}
            except Exception as e:
                return {'status': 'error', 'message': f'Error stopping graph: {str(e)}'}

    def send_message(self, graph_id: str, message: Dict) -> Dict:
        with self.lock:
            if graph_id not in self.graphs:
                return {'status': 'error', 'message': f'Graph {graph_id} not found'}
            try:
                graph = self.graphs[graph_id]
                if graph.send_message(message['target'], message['content']):
                    return {'status': 'success', 'message': f"Message sent to node {message['target']}"}
                else:
                    return {'status': 'error', 'message': f"Target node {message['target']} not found or queue full"}
            except Exception as e:
                return {'status': 'error', 'message': f'Error sending message: {str(e)}'}

    def get_graph_status(self, graph_id: str) -> Dict:
        with self.lock:
            if graph_id not in self.graphs:
                return {'status': 'error', 'message': f'Graph {graph_id} not found'}
            try:
                status = self.graphs[graph_id].get_status()
                return {'status': 'success', 'data': status}
            except Exception as e:
                return {'status': 'error', 'message': f'Error getting graph status: {str(e)}'}

    def list_graphs(self) -> Dict:
        with self.lock:
            try:
                graphs = [{'graph_id': graph_id, 'topology': graph.topology_type, 'node_count': len(graph.nodes)} for graph_id, graph in self.graphs.items()]
                return {'status': 'success', 'data': graphs}
            except Exception as e:
                return {'status': 'error', 'message': f'Error listing graphs: {str(e)}'}