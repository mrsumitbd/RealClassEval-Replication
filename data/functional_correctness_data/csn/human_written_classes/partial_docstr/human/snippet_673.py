class Subscriptions:
    """This class is used to list the datasets and geographies you have acquired a subscription (or valid license) for.

    This class won't show any dataset or geography tagged in the catalog as `is_public_data` since those data do not
    require a subscription.

    """

    def __init__(self, credentials):
        self._credentials = credentials
        self._filters = {'only_products': True}
        self._datasets = None
        self._geographies = None

    def __repr__(self):
        return 'Datasets: {0}\nGeographies: {1}'.format(self.datasets, self.geographies)

    @property
    def datasets(self):
        """List of :obj:`Dataset` you have a subscription for.

        Raises:
            CatalogError: if there's a problem when connecting to the catalog.

        """
        if self._datasets is None:
            from .dataset import Dataset
            self._datasets = Dataset.get_all(self._filters, self._credentials)
        return self._datasets

    @property
    def geographies(self):
        """List of :obj:`Geography` you have a subscription for.

        Raises:
            CatalogError: if there's a problem when connecting to the catalog.

        """
        if self._geographies is None:
            from .geography import Geography
            self._geographies = Geography.get_all(self._filters, self._credentials)
        return self._geographies