from typing import Literal
from memos.graph_dbs.item import GraphDBEdge, GraphDBNode

class QueueMessage:

    def __init__(self, op: Literal['add', 'remove', 'merge', 'update', 'end'], before_node: list[str] | list[GraphDBNode] | None=None, before_edge: list[str] | list[GraphDBEdge] | None=None, after_node: list[str] | list[GraphDBNode] | None=None, after_edge: list[str] | list[GraphDBEdge] | None=None):
        self.op = op
        self.before_node = before_node
        self.before_edge = before_edge
        self.after_node = after_node
        self.after_edge = after_edge

    def __str__(self) -> str:
        return f'QueueMessage(op={self.op}, before_node={(self.before_node if self.before_node is None else len(self.before_node))}, after_node={(self.after_node if self.after_node is None else len(self.after_node))})'

    def __lt__(self, other: 'QueueMessage') -> bool:
        op_priority = {'add': 2, 'remove': 2, 'merge': 1, 'end': 0}
        return op_priority[self.op] < op_priority[other.op]