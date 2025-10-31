from flask_resty.sorting import FieldOrderings, FieldSortingBase

class PaginationBase:
    """The base class for pagination components.

    Pagination components control the list view fetches individual pages of
    data, as opposed to the full collection. They handle limiting the number
    of returned records, and fetching additional records after the initial
    page.

    Subclasses must implement :py:meth:`get_page` to provide the pagination
    logic.
    """

    def adjust_sort_ordering(self, view, field_orderings: FieldOrderings) -> FieldOrderings:
        return field_orderings

    def get_page(self, query, view):
        """Restrict the specified query to a single page.

        :param query: The query to paginate.
        :type query: :py:class:`sqlalchemy.orm.query.Query`
        :param view: The view with the model we wish to paginate.
        :type view: :py:class:`ModelView`
        :return: The paginated query
        :rtype: :py:class:`sqlalchemy.orm.query.Query`
        :raises: A :py:class:`NotImplementedError` if no implementation is
            provided.
        """
        raise NotImplementedError()

    def get_item_meta(self, item, view):
        """Build pagination metadata for a single item.

        :param item: An instance of the :py:attr:`ModelView.model`.
        :type item: obj
        :param view: The view with the :py:attr:`ModelView.model`.
        :type view: :py:class:`ModelView`
        """
        return None