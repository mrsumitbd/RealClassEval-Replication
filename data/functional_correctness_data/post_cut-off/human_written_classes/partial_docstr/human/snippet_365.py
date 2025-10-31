import json
from typing import Any, Dict, List, Optional
from loguru import logger
from siirl.workers.dag.task_graph import TaskGraph
import yaml
from siirl.workers.dag.node import Node, NodeRole, NodeType

class DAGConfigLoader:
    """
    Loads, parses, and constructs TaskGraph objects from YAML or JSON files.
    """

    def __init__(self):
        pass

    @staticmethod
    def _parse_raw_config(raw_dag_config: Dict[str, Any], file_path: str) -> TaskGraph:
        """
        Helper function to parse and build a TaskGraph from a raw dictionary configuration.
        This function is called by load_dag_from_file to handle common logic after loading YAML/JSON.

        Args:
            raw_dag_config (Dict[str, Any]): The raw configuration dictionary loaded from the file.
            file_path (str): The path of the configuration file.

        Returns:
            TaskGraph: A TaskGraph object constructed from the configuration.
        """
        if not raw_dag_config:
            raise ValueError(f"The configuration file '{file_path}' is empty or has an incorrect format.")
        dag_id = raw_dag_config.get('dag_id')
        if not dag_id:
            raise ValueError(f"The 'dag_id' is missing in the configuration '{file_path}'.")
        description = raw_dag_config.get('description')
        global_config = raw_dag_config.get('global_config', {})
        if 'nodes' not in raw_dag_config:
            raise ValueError(f"The 'nodes' list is missing in the DAG configuration")
        nodes_list_config = raw_dag_config.get('nodes')
        if not isinstance(nodes_list_config, list):
            raise ValueError(f"The 'nodes' field in the configuration '{file_path}' must be a list.")
        dag_nodes: List[Node] = []
        node_ids = set()
        for i, node_config_dict in enumerate(nodes_list_config):
            if not isinstance(node_config_dict, dict):
                logger.warning(f"The configuration of the {i + 1}th node in the file '{file_path}' is not a dictionary and has been skipped.")
                continue
            node_id = node_config_dict.get('node_id')
            if not node_id:
                raise ValueError(f"The 'node_id' is missing in the configuration of the {i + 1}th node in the file '{file_path}'.")
            if node_id in node_ids:
                raise ValueError(f"Duplicate node ID '{node_id}' found in the configuration file '{file_path}'.")
            node_ids.add(node_id)
            if 'node_type' not in node_config_dict:
                raise ValueError(f"Node '{node_id}' is missing 'node_type'")
            node_type_str = node_config_dict.get('node_type').upper()
            try:
                node_type = NodeType[node_type_str]
            except KeyError:
                raise ValueError(f"The 'node_type' ('{node_type_str}') of node '{node_id}' in the file '{file_path}' is invalid.")
            node_role_str = node_config_dict.get('node_role', 'DEFAULT').upper()
            try:
                node_role = NodeRole[node_role_str]
            except KeyError:
                raise ValueError(f"The 'node_role' ('{node_role_str}') of node '{node_id}' in the file '{file_path}' is invalid.")
            only_forward_compute = node_config_dict.get('only_forward_compute', False)
            agent_group = node_config_dict.get('agent_group', 0)
            dependencies = node_config_dict.get('dependencies', [])
            if not isinstance(dependencies, list):
                raise ValueError(f"The 'dependencies' of node '{node_id}' in the file '{file_path}' must be a list.")
            node_specific_config = resolve_refs(node_config_dict.get('config', {}), global_config)
            executable_ref_str = node_config_dict.get('executable_ref')
            node_specific_config['_node_id_'] = node_id
            user_options = node_config_dict.get('user_options', {})
            dag_node = Node(node_id=node_id, node_type=node_type, node_role=node_role, only_forward_compute=only_forward_compute, agent_group=agent_group, dependencies=dependencies, config=node_specific_config, executable_ref=executable_ref_str, user_options=user_options)
            dag_nodes.append(dag_node)
        task_graph = TaskGraph(dag_id)
        task_graph.add_nodes(dag_nodes)
        task_graph.build_adjacency_lists()
        valid, msg = task_graph.validate_graph()
        if not valid:
            raise ValueError(f'The graph loaded from the configuration is invalid: {msg}')
        logger.info(f"TaskGraph '{dag_id}' built successfully with {len(task_graph.nodes)} nodes")
        return task_graph

    @staticmethod
    def load_from_file(file_path: str, file_type: str='yaml') -> TaskGraph:
        """
        Loads and constructs a TaskGraph from the specified YAML or JSON file.
        Determines the file type based on file_type.

        Args:
            file_path (str): The path of the configuration file.
            file_type (str): The type of the configuration file, default is yaml

        Returns:
            TaskGraph: A TaskGraph object constructed from the configuration file.
        """
        raw_dag_config: Optional[Dict[str, Any]] = None
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                if file_type in ['yaml', 'yml']:
                    raw_dag_config = yaml.safe_load(f)
                elif file_type == 'json':
                    raw_dag_config = json.load(f)
                else:
                    raise ValueError(f"Unsupported file type: '{file_type}'. Please use yaml, yml, or json.")
        except FileNotFoundError:
            logger.error(f"The configuration file '{file_path}' was not found.")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Failed to parse the YAML file '{file_path}': {e}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse the JSON file '{file_path}': {e}")
            raise
        except Exception as e:
            logger.error(f"An unknown error occurred while loading the configuration file '{file_path}': {e}")
            raise
        if raw_dag_config is None:
            raise ValueError(f"The result of loading the configuration file '{file_path}' is empty. It might be an empty file or have a format issue.")
        return DAGConfigLoader._parse_raw_config(raw_dag_config, file_path)