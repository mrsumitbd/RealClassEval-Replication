class Fact:
    """This object represents a fact. Unless otherwise specified all
    parameters are required.

    :param node: The hostname this fact was collected from.
    :type node: :obj:`string`
    :param name: The fact's name, such as 'osfamily'
    :type name: :obj:`string`
    :param value: The fact's value, such as 'Debian'
    :type value: :obj:`string` or :obj:`int` or :obj:`dict`
    :param environment: (Optional) The fact's environment, such as        'production'
    :type environment: :obj:`string`

    :ivar node: :obj:`string` holding the hostname.
    :ivar name: :obj:`string` holding the fact's name.
    :ivar value: :obj:`string` or :obj:`int` or :obj:`dict` holding the        fact's value.
    :ivar environment: :obj:`string` holding the fact's environment
    """

    @staticmethod
    def create_from_dict(fact):
        return Fact(node=fact['certname'], name=fact['name'], value=fact['value'], environment=fact['environment'])

    def __init__(self, node, name, value, environment=None):
        self.node = node
        self.name = name
        self.value = value
        self.environment = environment
        self.__string = f'{self.name}/{self.node}'

    def __repr__(self):
        return str(f'Fact: {self.__string}')

    def __str__(self):
        return '{}'.format(self.__string)