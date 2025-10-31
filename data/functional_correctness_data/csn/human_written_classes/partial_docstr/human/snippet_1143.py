class AtlasPagination:
    """Atlas Pagination Generic Implementation

    Constructor

    Args:
        atlas (Atlas): Atlas instance
        fetch (function): The function "get_all" to call
        pageNum (int): Page number
        itemsPerPage (int): Number of Users per Page
    """

    def __init__(self, atlas, fetch, pageNum: int, itemsPerPage: int):
        self.atlas = atlas
        self.fetch = fetch
        self.pageNum = pageNum
        self.itemsPerPage = itemsPerPage

    def __iter__(self):
        """Iterable

        Yields:
            str: One result
        """
        pageNum = self.pageNum
        total = pageNum * self.itemsPerPage
        while pageNum * self.itemsPerPage - total < self.itemsPerPage:
            try:
                details = self.fetch(pageNum, self.itemsPerPage)
            except Exception as e:
                raise ErrPagination(e)
            total = details['totalCount']
            results = details['results']
            results_count = len(results)
            index = 0
            while index < results_count:
                result = results[index]
                index += 1
                yield result

            class DatabaseUsersGetAll(AtlasPagination):
                """Pagination for Database User : Get All"""

                def __init__(self, atlas, pageNum, itemsPerPage):
                    super().__init__(atlas, atlas.DatabaseUsers.get_all_database_users, pageNum, itemsPerPage)
            pageNum += 1