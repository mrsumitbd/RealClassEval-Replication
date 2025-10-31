class MonitoringTransaction:
    """
    Represents a monitoring transaction (likely the current transaction).
    """

    def __init__(self, transaction):
        self.transaction = transaction

    @property
    def name(self):
        """
        The name of the transaction.

        For NewRelic, the name may look like:
            openedx.core.djangoapps.contentserver.middleware:StaticContentServer

        """
        if self.transaction and hasattr(self.transaction, 'name'):
            return self.transaction.name
        return None