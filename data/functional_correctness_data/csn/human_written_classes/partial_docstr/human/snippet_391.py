import time

class Proxy:
    """Proxy class

    Attributes:
        addr (str): A string with IP and port, for example '123.123.123.123:8080'
        protocol (str): 'http' or 'https'
        weight (float): A float point number indicating the probability of being
            selected, the weight is based on the connection time and stability
        last_checked (time): A UNIX timestamp indicating when the proxy was checked
    """

    def __init__(self, addr=None, protocol='http', weight=1.0, last_checked=None):
        self.addr = addr
        self.protocol = protocol
        self.weight = weight
        if last_checked is None:
            self.last_checked = int(time.time())
        else:
            self.last_checked = last_checked

    def format(self):
        """Return the proxy compatible with requests.Session parameters

        Returns:
            dict: A dict like {'http': '123.123.123.123:8080'}
        """
        return {self.protocol: self.addr}

    def to_dict(self):
        """convert detailed proxy info into a dict

        Returns:
            dict: A dict with four keys: ``addr``, ``protocol``,
                  ``weight`` and ``last_checked``
        """
        return {'addr': self.addr, 'protocol': self.protocol, 'weight': self.weight, 'last_checked': self.last_checked}