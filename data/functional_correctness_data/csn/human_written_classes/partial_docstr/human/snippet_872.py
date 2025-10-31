from pypuppetdb.utils import json_to_datetime

class Event:
    """This object represents an event. Unless otherwise specified all
    parameters are required.

    :param node: The hostname of the node this event fired on.
    :type node: :obj:`string`
    :param status: The status for the event.
    :type status: :obj:`string`
    :param timestamp: A timestamp of when this event occured.
    :type timestamp: :obj:`string` formatted as ``%Y-%m-%dT%H:%M:%S.%fZ``
    :param hash_: The hash of the report that contains this event.
    :type hash_: :obj:`string`
    :param title: The resource title this event was fired for.
    :type title: :obj:`string`
    :param property_: The property of the resource this event was fired for.
    :type property_: :obj:`string`
    :param message: A message associated with this event.
    :type message: :obj:`string`
    :param new_value: The new value/state of the resource.
    :type new_value: :obj:`string`
    :param old_value: The old value/state of the resource.
    :type old_value: :obj:`string`
    :param type_: The type of the resource this event fired for.
    :type type_: :obj:`string`
    :param class_: The class responsible for running this event.
    :type class_: :obj:`string`
    :param execution_path: The path used to reach this particular resource.
    :type execution_path: :obj:`string`
    :param source_file: The puppet source code file containing the class.
    :type source_file: :obj:`string`
    :param line_number: The line number in the source file containing the
        definition responsible for triggering this event.
    :type line_number: :obj:`int`

    :ivar node: A :obj:`string` of this event's node certname.
    :ivar status: A :obj:`string` of this event's status.
    :ivar failed: The :obj:`bool` equivalent of `status`.
    :ivar timestamp: A :obj:`datetime.datetime` of when this event happend.
    :ivar node: The hostname of the machine this event        occured on.
    :ivar hash_: The hash of this event.
    :ivar item: :obj:`dict` with information about the item/resource this        event was triggered for.
    """

    def __init__(self, node, status, timestamp, hash_, title, property_, message, new_value, old_value, type_, class_, execution_path, source_file, line_number):
        self.node = node
        self.status = status
        if self.status == 'failure':
            self.failed = True
        else:
            self.failed = False
        self.timestamp = json_to_datetime(timestamp)
        self.hash_ = hash_
        self.item = {'title': title, 'type': type_, 'property': property_, 'message': message, 'old': old_value, 'new': new_value, 'class': class_, 'execution_path': execution_path, 'source_file': source_file, 'line_number': line_number}
        self.__string = '{}[{}]/{}'.format(self.item['type'], self.item['title'], self.hash_)

    def __repr__(self):
        return str(f'Event: {self.__string}')

    def __str__(self):
        return '{}'.format(self.__string)

    @staticmethod
    def create_from_dict(event):
        return Event(node=event['certname'], status=event['status'], timestamp=event['timestamp'], hash_=event['report'], title=event['resource_title'], property_=event['property'], message=event['message'], new_value=event['new_value'], old_value=event['old_value'], type_=event['resource_type'], class_=event['containing_class'], execution_path=event['containment_path'], source_file=event['file'], line_number=event['line'])