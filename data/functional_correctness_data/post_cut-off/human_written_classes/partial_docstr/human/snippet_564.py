from rich.tree import Tree
from rich.panel import Panel
from typing import Dict, List, Optional, Union, Tuple

class MetricTreePanel:
    """Displays the solution tree with depth limiting."""

    def __init__(self, maximize: bool):
        self.metric_tree = MetricTree(maximize=maximize)

    def build_metric_tree(self, nodes: List[dict]):
        """Build the tree from the list of nodes."""
        if nodes is None:
            nodes = []
        self.metric_tree.clear()
        nodes.sort(key=lambda x: x['step'])
        for i, node in enumerate(nodes):
            node = Node(id=node['solution_id'], parent_id=node['parent_id'], code=node['code'], metric=node['metric_value'], is_buggy=node['is_buggy'])
            if i == 0:
                node.name = 'baseline'
            self.metric_tree.add_node(node)

    def set_unevaluated_node(self, node_id: str):
        """Set the unevaluated node."""
        self.metric_tree.nodes[node_id].evaluated = False

    def _build_rich_tree(self) -> Tree:
        """Get a Rich Tree representation of the solution tree using a DFS like traversal."""
        if len(self.metric_tree.nodes) == 0:
            return Tree('[bold green]Building first solution...')
        best_node = self.metric_tree.get_best_node()

        def append_rec(node: Node, tree: Tree):
            if not node.evaluated:
                color = 'yellow'
                style = None
                text = 'evaluating...'
            elif node.is_buggy:
                color = 'red'
                style = None
                text = 'bug'
            else:
                if node.id == best_node.id:
                    color = 'green'
                    style = 'bold'
                    text = f'{node.metric:.3f} 🏆'
                elif node.metric is None:
                    color = 'yellow'
                    style = None
                    text = 'N/A'
                else:
                    color = 'green'
                    style = None
                    text = f'{node.metric:.3f}'
                text = f'{node.name} {text}'.strip()
            s = f"[{(f'{style} ' if style is not None else '')}{color}]● {text}"
            subtree = tree.add(s)
            for child in node.children:
                append_rec(child, subtree)
        tree = Tree('', hide_root=True)
        root_node = self.metric_tree.get_root_node()
        append_rec(node=root_node, tree=tree)
        return tree

    def get_display(self, is_done: bool) -> Panel:
        """Get a panel displaying the solution tree."""
        return Panel(self._build_rich_tree(), title='[bold]🔎 Exploring Solutions...' if not is_done else '[bold]🔎 Optimization Complete!', border_style='green', expand=True, padding=(0, 1))