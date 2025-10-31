class Resource:
    """This object represents a resource. Unless otherwise specified all
    parameters are required.

    :param node: The hostname this resource is located on.
    :type node: :obj:`string`
    :param name: The name of the resource in the Puppet manifest.
    :type name: :obj:`string`
    :param type_: Type of the Puppet resource.
    :type type_: :obj:`string`
    :param tags: Tags associated with this resource.
    :type tags: :obj:`list`
    :param exported: If it's an exported resource.
    :type exported: :obj:`bool`
    :param sourcefile: The Puppet manifest this resource is declared in.
    :type sourcefile: :obj:`string`
    :param sourceline: The line this resource is declared at.
    :type sourceline: :obj:`int`
    :param parameters: (Optional) The parameters this resource has been        declared with.
    :type parameters: :obj:`dict`
    :param environment: (Optional) The environment of the node associated        with this resource.
    :type environment: :obj:`string`

    :ivar node: The hostname this resources is located on.
    :ivar name: The name of the resource in the Puppet manifest.
    :ivar type_: The type of Puppet resource.
    :ivar exported: :obj:`bool` if the resource is exported.
    :ivar sourcefile: The Puppet manifest this resource is declared in.
    :ivar sourceline: The line this resource is declared at.
    :ivar parameters: :obj:`dict` with key:value pairs of parameters.
    :ivar relationships: :obj:`list` Contains all relationships to other        resources
    :ivar environment: :obj:`string` The environment of the node associated        with this resource.
    """

    def __init__(self, node, name, type_, tags, exported, sourcefile, sourceline, environment=None, parameters={}):
        self.node = node
        self.name = name
        self.type_ = type_
        self.tags = tags
        self.exported = exported
        self.sourcefile = sourcefile
        self.sourceline = sourceline
        self.parameters = parameters
        self.relationships = []
        self.environment = environment
        self.__string = f'{self.type_}[{self.name}]'

    def __repr__(self):
        return '<Resource: {}>'.format(self.__string)

    def __str__(self):
        return '{}'.format(self.__string)

    @staticmethod
    def create_from_dict(resource):
        return Resource(node=resource['certname'], name=resource['title'], type_=resource['type'], tags=resource['tags'], exported=resource['exported'], sourcefile=resource['file'], sourceline=resource['line'], parameters=resource['parameters'], environment=resource['environment'])