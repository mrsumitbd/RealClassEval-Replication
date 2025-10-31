class SubscriptionType:
    """
    Databox class representing a type of subscription to OpenWeatherMap web APIs

    :param name: the name of the subscription
    :type name: str
    :param subdomain: the root API subdomain associated to the subscription
    :type subdomain: str
    :param is_paid: tells if the subscription plan is paid
    :type is_paid: bool
    """

    def __init__(self, name, subdomain, is_paid):
        self.name = name
        self.subdomain = subdomain
        self.is_paid = is_paid

    def __repr__(self):
        return '<%s.%s - name=%s subdomain=%s paid=%s>' % (__name__, self.__class__.__name__, self.name, self.subdomain, self.is_paid)