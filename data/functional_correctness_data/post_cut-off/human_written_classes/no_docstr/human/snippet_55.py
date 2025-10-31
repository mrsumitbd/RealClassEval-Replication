from typing import List, Optional, Tuple, Dict
import torch

class InterventionGraph:
    prompt: str
    ordered_nodes: List['Supernode']
    nodes: Dict[str, 'Supernode']

    def __init__(self, ordered_nodes: List['Supernode'], prompt: str):
        self.ordered_nodes = ordered_nodes
        self.prompt = prompt
        self.nodes = {}

    def initialize_node(self, node, activations):
        self.nodes[node.name] = node
        if node.features:
            node.default_activations = torch.tensor([activations[feature] for feature in node.features])
        else:
            node.default_activations = None

    def set_node_activation_fractions(self, current_activations):
        for node in self.nodes.values():
            if node.features:
                current_node_activation = torch.tensor([current_activations[feature] for feature in node.features])
                node.activation = (current_node_activation / node.default_activations).mean().item()
            else:
                node.activation = None
            node.intervention = None
            node.replacement_node = None