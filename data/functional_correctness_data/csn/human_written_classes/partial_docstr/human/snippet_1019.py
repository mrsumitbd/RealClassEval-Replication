import typing

class SWCNode:
    """
    Represents a single node in an SWC (Standardized Morphology Data Format) file.

    The SWC format is a widely used standard for representing neuronal morphology data.
    It consists of a series of lines, each representing a single node or sample point
    along the neuronal structure. For more information on the SWC format, see:
    https://swc-specification.readthedocs.io/en/latest/swc.html

    :param UNDEFINED: ID representing an undefined node type
    :type UNDEFINED: int
    :param SOMA: ID representing a soma node
    :type SOMA: int
    :param AXON: ID representing an axon node
    :type AXON: int
    :param BASAL_DENDRITE: ID representing a basal dendrite node
    :type BASAL_DENDRITE: int
    :param APICAL_DENDRITE: ID representing an apical dendrite node
    :type APICAL_DENDRITE: int
    :param CUSTOM: ID representing a custom node type
    :type CUSTOM: int
    :param UNSPECIFIED_NEURITE: ID representing an unspecified neurite node
    :type UNSPECIFIED_NEURITE: int
    :param GLIA_PROCESSES: ID representing a glia process node
    :type GLIA_PROCESSES: int
    :param TYPE_NAMES: A mapping of node type IDs to their string representations
    :type TYPE_NAMES: dict
    """
    UNDEFINED = 0
    SOMA = 1
    AXON = 2
    BASAL_DENDRITE = 3
    APICAL_DENDRITE = 4
    CUSTOM = 5
    UNSPECIFIED_NEURITE = 6
    GLIA_PROCESSES = 7
    TYPE_NAMES = {UNDEFINED: 'Undefined', SOMA: 'Soma', AXON: 'Axon', BASAL_DENDRITE: 'Basal Dendrite', APICAL_DENDRITE: 'Apical Dendrite', CUSTOM: 'Custom', UNSPECIFIED_NEURITE: 'Unspecified Neurite', GLIA_PROCESSES: 'Glia Processes'}

    def __init__(self, node_id: typing.Union[str, int], type_id: typing.Union[str, int], x: typing.Union[str, float], y: typing.Union[str, float], z: typing.Union[str, float], radius: typing.Union[str, float], parent_id: typing.Union[str, int]):
        try:
            self.id = int(node_id)
            self.type = int(type_id)
            self.x = float(x)
            self.y = float(y)
            self.z = float(z)
            self.radius = float(radius)
            self.parent_id = int(parent_id)
            self.children: typing.List[SWCNode] = []
        except (ValueError, TypeError) as e:
            raise ValueError(f'Invalid data types in SWC line: {e}')

    def __str__(self) -> str:
        """
        Returns a human-readable string representation of the node.

        :return: A string representation of the node
        :rtype: str
        """
        type_name = self.TYPE_NAMES.get(self.type, f'Custom_{self.type}')
        return f'Node ID: {self.id}, Type: {type_name}, Coordinates: ({self.x:.2f}, {self.y:.2f}, {self.z:.2f}), Radius: {self.radius:.2f}, Parent ID: {self.parent_id}'