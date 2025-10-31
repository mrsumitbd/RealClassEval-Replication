from urllib.parse import urlparse
from coapthon.utils import parse_uri

class CoapUri:
    """ Class that can manage and inbox the CoAP URI """

    def __init__(self, coap_uri):
        self.uri = coap_uri
        self.host, self.port, self.path = parse_uri(coap_uri)

    def get_uri_as_list(self):
        """
        Split the uri into <scheme>://<netloc>/<path>;<params>?<query>#<fragment>

        :return: the split uri
        """
        return urlparse(self.uri)

    def get_payload(self):
        """
        Return the query string of the uri.

        :return: the query string as a list
        """
        temp = self.get_uri_as_list()
        query_string = temp[4]
        if query_string == '':
            return None
        query_string_as_list = str.split(query_string, '=')
        return query_string_as_list[1]

    def __str__(self):
        return self.uri