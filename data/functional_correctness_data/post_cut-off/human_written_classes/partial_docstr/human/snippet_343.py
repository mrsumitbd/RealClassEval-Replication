import sys

class N8nWorkflowParser:
    """
    Parses n8n workflow JSON into a standardized graph format,
    including synthetic _START_ and _END_ nodes.
    """

    def __init__(self, n8n_data, filename, categories_data):
        self.n8n_data = n8n_data
        self.filename = filename
        self.categories_data = categories_data
        self.nodes = []
        self.edges = []
        self.node_map_by_id = {}
        self.node_map_by_name = {}
        self.parsed_node_ids = set()

    def _determine_node_type(self, n8n_node_name):
        """Determines node type based on node name."""
        if not n8n_node_name:
            return 'Generic'
        name_lower = n8n_node_name.lower()
        if 'agent' in name_lower:
            return 'Agent'
        elif 'tool' in name_lower:
            return 'Tool'
        else:
            return 'Generic'

    def _parse_nodes(self):
        """Extracts and formats node information from n8n data."""
        if 'nodes' not in self.n8n_data or not isinstance(self.n8n_data['nodes'], list):
            print(f"Warning ({self.filename}): 'nodes' array not found or invalid.", file=sys.stderr)
            return
        for node_data in self.n8n_data['nodes']:
            node_id = node_data.get('id')
            if not node_id:
                print(f"Warning ({self.filename}): Skipping node without an 'id': {node_data.get('name', 'Unnamed')}", file=sys.stderr)
                continue
            node_type_raw = node_data.get('type', 'Unknown')
            if node_type_raw == 'n8n-nodes-base.stickyNote':
                continue
            self.parsed_node_ids.add(node_id)
            n8n_node_name = node_data.get('name', '')
            description = n8n_node_name if n8n_node_name else node_id
            output_node_type = self._determine_node_type(n8n_node_name)
            simplified_type_meta = simplify_n8n_type(node_type_raw)
            docstring = node_data.get('notes')
            docstring = docstring if docstring else None
            parameters = node_data.get('parameters', {})
            category_data = self.categories_data.get(node_type_raw, {})
            categories_list = category_data.get('categories', [])
            subcategories_data = category_data.get('subcategories', [])
            primary_category = categories_list[0] if categories_list else None
            primary_subcategory = None
            if primary_category:
                if isinstance(subcategories_data, list):
                    primary_subcategory = subcategories_data[0] if subcategories_data else None
                elif isinstance(subcategories_data, dict):
                    subcats_for_primary = subcategories_data.get(primary_category, [])
                    if isinstance(subcats_for_primary, list) and subcats_for_primary:
                        primary_subcategory = subcats_for_primary[0]
            node_output = {'name': node_id, 'function_name': node_id, 'docstring': docstring, 'description': description, 'node_type': output_node_type, 'source_location': self.filename, 'metadata': {'n8n_id': node_id, 'n8n_type': node_type_raw, 'simplified_n8n_type': simplified_type_meta, 'category': primary_category, 'subcategory': primary_subcategory, 'n8n_categories_list': categories_list, 'n8n_subcategories_data': subcategories_data, 'parameters': parameters}}
            self.nodes.append(node_output)
            self.node_map_by_id[node_id] = node_data
            if n8n_node_name in self.node_map_by_name:
                print(f"Warning ({self.filename}): Duplicate node name '{n8n_node_name}'. Connection mapping might use the first encountered ID.", file=sys.stderr)
            elif n8n_node_name:
                self.node_map_by_name[n8n_node_name] = node_id

    def _parse_edges(self):
        """Extracts and formats edge information from n8n connections."""
        connections = self.n8n_data.get('connections', {})
        if not isinstance(connections, dict):
            print(f"Warning ({self.filename}): 'connections' is not a dictionary. Found type: {type(connections)}. Skipping edge parsing.", file=sys.stderr)
            return
        for source_node_name, outputs in connections.items():
            source_node_id = self.node_map_by_name.get(source_node_name)
            if not source_node_id:
                if source_node_name in self.node_map_by_id:
                    source_node_id = source_node_name
                else:
                    print(f"Warning ({self.filename}): Could not find source node ID for name '{source_node_name}' in connections. Skipping connections from this node.", file=sys.stderr)
                    continue
            if source_node_id not in self.parsed_node_ids:
                continue
            if not isinstance(outputs, dict):
                print(f"Warning ({self.filename}): Expected dictionary for outputs of node '{source_node_name}', found {type(outputs)}. Skipping.", file=sys.stderr)
                continue
            for output_handle, targets_array in outputs.items():
                if not isinstance(targets_array, list):
                    print(f"Warning ({self.filename}): Expected list for targets from '{source_node_name}' output '{output_handle}', found {type(targets_array)}. Skipping.", file=sys.stderr)
                    continue
                for target_list in targets_array:
                    if not isinstance(target_list, list):
                        print(f"Warning ({self.filename}): Expected inner list for targets from '{source_node_name}' output '{output_handle}', found {type(target_list)}. Skipping.", file=sys.stderr)
                        continue
                    for target_info in target_list:
                        if not isinstance(target_info, dict):
                            print(f"Warning ({self.filename}): Expected dictionary for target info from '{source_node_name}' output '{output_handle}', found {type(target_info)}. Skipping.", file=sys.stderr)
                            continue
                        target_node_name = target_info.get('node')
                        target_input_handle = target_info.get('type', 'main')
                        if not target_node_name:
                            print(f"Warning ({self.filename}): Target connection from '{source_node_name}' (ID: {source_node_id}) via handle '{output_handle}' is missing target node name. Skipping.", file=sys.stderr)
                            continue
                        target_node_id = self.node_map_by_name.get(target_node_name)
                        if not target_node_id:
                            if target_node_name in self.node_map_by_id:
                                target_node_id = target_node_name
                            else:
                                print(f"Warning ({self.filename}): Could not find target node ID for name '{target_node_name}' connected from '{source_node_name}' (ID: {source_node_id}). Skipping this edge.", file=sys.stderr)
                                continue
                        if target_node_id not in self.parsed_node_ids:
                            print(f"Info ({self.filename}): Skipping edge to filtered node '{target_node_name}' (ID: {target_node_id}). It might be a StickyNote.", file=sys.stderr)
                            continue
                        edge_output = {'source': source_node_id, 'target': target_node_id, 'condition': output_handle, 'metadata': {'definition_location': self.filename, 'source_handle': output_handle, 'target_handle': target_input_handle}}
                        self.edges.append(edge_output)

    def _add_start_end_nodes(self):
        """Adds synthetic _START_ and _END_ nodes and their edges."""
        if not self.parsed_node_ids:
            print(f'Info ({self.filename}): No functional nodes found, skipping _START_/_END_ node addition.')
            return
        start_node = {'name': '_START_', 'function_name': '_START_', 'docstring': 'Synthetic node representing the workflow entry point(s).', 'description': 'Workflow Start', 'node_type': 'WorkflowBoundary', 'source_location': self.filename, 'metadata': {'n8n_id': '_START_', 'n8n_type': 'synthetic.start', 'simplified_n8n_type': 'StartBoundary', 'category': 'Workflow', 'subcategory': 'Boundary', 'n8n_categories_list': ['Workflow'], 'n8n_subcategories_data': ['Boundary'], 'parameters': {}}}
        end_node = {'name': '_END_', 'function_name': '_END_', 'docstring': 'Synthetic node representing the workflow terminal point(s).', 'description': 'Workflow End', 'node_type': 'WorkflowBoundary', 'source_location': self.filename, 'metadata': {'n8n_id': '_END_', 'n8n_type': 'synthetic.end', 'simplified_n8n_type': 'EndBoundary', 'category': 'Workflow', 'subcategory': 'Boundary', 'n8n_categories_list': ['Workflow'], 'n8n_subcategories_data': ['Boundary'], 'parameters': {}}}
        source_ids_in_edges = {edge['source'] for edge in self.edges}
        target_ids_in_edges = {edge['target'] for edge in self.edges}
        actual_start_node_ids = self.parsed_node_ids - target_ids_in_edges
        actual_end_node_ids = self.parsed_node_ids - source_ids_in_edges
        new_nodes = [start_node] + self.nodes + [end_node]
        new_edges = list(self.edges)
        for start_id in actual_start_node_ids:
            new_edges.append({'source': '_START_', 'target': start_id, 'condition': 'trigger', 'metadata': {'definition_location': self.filename, 'source_handle': 'start', 'target_handle': 'input'}})
        for end_id in actual_end_node_ids:
            new_edges.append({'source': end_id, 'target': '_END_', 'condition': 'terminal', 'metadata': {'definition_location': self.filename, 'source_handle': 'output', 'target_handle': 'end'}})
        self.nodes = new_nodes
        self.edges = new_edges

    def parse(self):
        """Parses the entire workflow and returns the structured output."""
        self._parse_nodes()
        if self.parsed_node_ids:
            self._parse_edges()
            self._add_start_end_nodes()
        else:
            pass
        return {'nodes': self.nodes, 'edges': self.edges}