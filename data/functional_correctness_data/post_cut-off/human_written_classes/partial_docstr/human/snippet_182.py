class CallGraph:

    def __init__(self, nodes=None, edges=None):
        self.nodes = nodes if nodes is not None else {}
        self.edges = edges if edges is not None else []
        self._edge_set = set()

    def add_node(self, node):
        if node.fully_qualified_name not in self.nodes:
            self.nodes[node.fully_qualified_name] = node

    def add_edge(self, src_name, dst_name):
        if src_name not in self.nodes or dst_name not in self.nodes:
            raise ValueError('Both source and destination nodes must exist in the graph.')
        edge_key = (src_name, dst_name)
        if edge_key in self._edge_set:
            return
        edge = Edge(self.nodes[src_name], self.nodes[dst_name])
        self.edges.append(edge)
        self._edge_set.add(edge_key)
        self.nodes[src_name].added_method_called_by_me(self.nodes[dst_name])

    def __str__(self):
        result = f'Control flow graph with {len(self.nodes)} nodes and {len(self.edges)} edges\n'
        for _, node in self.nodes.items():
            if node.methods_called_by_me:
                result += f"Method {node.fully_qualified_name} is calling the following methods: {', '.join(node.methods_called_by_me)}\n"
        return result

    def llm_str(self, size_limit=2500000):
        """
        Return a string representation with size limits.
        If output exceeds size_limit, group method calls by class.
        """
        default_str = str(self)
        logger.info(f'[CFG Tool] LLM string: {len(default_str)} characters, size limit: {size_limit} characters')
        if len(default_str) <= size_limit:
            return default_str
        class_calls = {}
        function_calls = []
        logger.info(f'[CallGraph] Control flow graph is too large, grouping method calls by class. ({len(default_str)} characters)')
        for _, node in self.nodes.items():
            if node.type == 6 and node.methods_called_by_me:
                parts = node.fully_qualified_name.split('.')
                if len(parts) > 1:
                    class_name = '.'.join(parts[:-1])
                    if class_name not in class_calls:
                        class_calls[class_name] = {}
                    for called_method in node.methods_called_by_me:
                        called_parts = called_method.split('.')
                        if len(called_parts) > 1:
                            called_class = '.'.join(called_parts[:-1])
                            if called_class not in class_calls[class_name]:
                                class_calls[class_name][called_class] = 0
                            class_calls[class_name][called_class] += 1
                        else:
                            if called_method not in class_calls[class_name]:
                                class_calls[class_name][called_method] = 0
                            class_calls[class_name][called_method] += 1
                else:
                    function_calls.append(f"Function {node.fully_qualified_name} is calling the following methods: {', '.join(node.methods_called_by_me)}")
            elif node.methods_called_by_me:
                function_calls.append(f"Function {node.fully_qualified_name} is calling the following methods: {', '.join(node.methods_called_by_me)}")
        result = f'Control flow graph with {len(self.nodes)} nodes and {len(self.edges)} edges (grouped view)\n'
        for class_name, called_classes in class_calls.items():
            calls_str = []
            for called_class, count in called_classes.items():
                calls_str.append(f'{called_class}({count} methods)')
            if calls_str:
                result += f"Class {class_name} is calling the following classes {', '.join(calls_str)}\n"
        for func_call in function_calls:
            result += func_call + '\n'
        logger.info(f'[CallGraph] Control flow graph grouped by class, total characters: {len(result)}')
        return result