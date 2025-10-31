from pypuppetdb.utils import json_to_datetime

class Inventory:
    """This object represents a Node Inventory entry returned from
    the Inventory endpoint.

    :param node: The certname of the node associated with the inventory.
    :type node: :obj:`string`
    :param time: The time at which PuppetDB received the facts in the
        inventory.
    :type time: :obj:`string` formatted as ``%Y-%m-%dT%H:%M:%S.%fZ``
    :param environment: The environment associated with the inventory's
        certname.
    :type environment: :obj:`string`
    :param facts: The dictionary of key-value pairs for the nodes
        assosciated facts.
    :type facts: :obj:`dict`
    :param trusted: The trusted data from the node.
    :type trusted: :obj:`dict`

    :ivar node: The certname of the node associated with the inventory.
    :ivar time: The time at which PuppetDB received the facts in the
        inventory.
    :ivar environment: The environment associated with the inventory's
        certname.
    :ivar facts: The dictionary of key-value pairs for the nodes
        assosciated facts.
    :ivar trusted: The trusted data from the node.
    """

    def __init__(self, node, time, environment, facts, trusted):
        self.node = node
        self.time = json_to_datetime(time)
        self.environment = environment
        self.facts = facts
        self.trusted = trusted
        self.__string = self.node

    def __repr__(self):
        return '<Inventory: {}>'.format(self.__string)

    def __str__(self):
        return '{}'.format(self.__string)

    @staticmethod
    def create_from_dict(inv):
        return Inventory(node=inv['certname'], time=inv['timestamp'], environment=inv['environment'], facts=inv['facts'], trusted=inv['trusted'])