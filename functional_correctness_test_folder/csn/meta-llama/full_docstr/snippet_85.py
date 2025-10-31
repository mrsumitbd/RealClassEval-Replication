
class SessionListener:
    '''Base class for :class:`Session` listeners, which are notified when a new
    NETCONF message is received or an error occurs.
    .. note::
        Avoid time-intensive tasks in a callback's context.
    '''

    def callback(self, root, raw):
        '''Called when a new XML document is received. The *root* argument allows the callback to determine whether it wants to further process the document.
        Here, *root* is a tuple of *(tag, attributes)* where *tag* is the qualified name of the root element and *attributes* is a dictionary of its attributes (also qualified names).
        *raw* will contain the XML document as a string.
        '''
        pass

    def errback(self, ex):
        '''Called when an error occurs.
        :type ex: :exc:`Exception`
        '''
        pass


class ExampleSessionListener(SessionListener):
    def __init__(self, logger=None):
        self.logger = logger

    def callback(self, root, raw):
        tag, attributes = root
        if self.logger:
            self.logger.info(
                f'Received XML document with root tag {tag} and attributes {attributes}')
        # Process the XML document further if needed
        # For example, parse the XML document using an XML parser like xml.etree.ElementTree
        import xml.etree.ElementTree as ET
        try:
            root_element = ET.fromstring(raw)
            # Process the root element
            if self.logger:
                self.logger.info(f'Parsed XML document: {root_element.tag}')
        except ET.ParseError as e:
            if self.logger:
                self.logger.error(f'Failed to parse XML document: {e}')

    def errback(self, ex):
        if self.logger:
            self.logger.error(f'An error occurred: {ex}')


# Example usage
if __name__ == '__main__':
    import logging

    # Create a logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Create a console handler and set the log level to INFO
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # Create a formatter and attach it to the console handler
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    # Add the console handler to the logger
    logger.addHandler(ch)

    # Create an instance of ExampleSessionListener with the logger
    listener = ExampleSessionListener(logger)

    # Simulate receiving an XML document
    root = ('example:root', {'xmlns:example': 'http://example.com'})
    raw = '<example:root xmlns:example="http://example.com"><example:element>data</example:element></example:root>'
    listener.callback(root, raw)

    # Simulate an error occurring
    try:
        raise Exception('Simulated error')
    except Exception as ex:
        listener.errback(ex)
