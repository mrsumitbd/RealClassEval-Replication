class Edge:
    """
    This object represents the connection between two Resource objects.
    Unless otherwise specified all parameters are required.

    :param source: The source Resource object of the relationship
    :type source: :class:`pypuppetdb.Resource`
    :param target: The target Resource object of the relationship
    :type target: :class:`pypuppetdb.Resource`
    :param relationship: Name of the Puppet Resource Relationship
    :type relationship: :obj:`string`
    :param node: The certname of the node that owns this Relationship
    :type node: :obj:`string`

    :ivar source: :obj:`Resource` The source Resource object
    :ivar target: :obj:`Resource` The target Resource object
    :ivar relationship: :obj:`string` Name of the Puppet Resource relationship
    :ivar node: :obj:`string` The name of the node that owns this relationship
    """

    def __init__(self, source, target, relationship, node=None):
        self.source = source
        self.target = target
        self.relationship = relationship
        self.node = node
        self.__string = '{} - {} - {}'.format(self.source, self.relationship, self.target)

    def __repr__(self):
        return '<Edge: {}>'.format(self.__string)

    def __str__(self):
        return '{}'.format(self.__string)

    @staticmethod
    def create_from_dict(edge):
        identifier_source = edge['source_type'] + '[' + edge['source_title'] + ']'
        identifier_target = edge['target_type'] + '[' + edge['target_title'] + ']'
        return Edge(source=identifier_source, target=identifier_target, relationship=edge['relationship'], node=edge['certname'])