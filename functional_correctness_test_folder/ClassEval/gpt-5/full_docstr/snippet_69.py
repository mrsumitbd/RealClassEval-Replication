class PageUtil:
    """
    PageUtil class is a versatile utility for handling pagination and search functionalities in an efficient and convenient manner.
    """

    def __init__(self, data, page_size):
        """
        Initialize the PageUtil object with the given data and page size.
        :param data: list, the data to be paginated
        :param page_size: int, the number of items per page
        """
        if page_size <= 0:
            raise ValueError("page_size must be a positive integer")
        self.data = list(data)
        self.page_size = int(page_size)
        self.total_items = len(self.data)
        self.total_pages = (self.total_items + self.page_size -
                            1) // self.page_size if self.total_items else 0

    def get_page(self, page_number):
        """
        Retrieve a specific page of data.
        :param page_number: int, the page number to fetch
        :return: list, the data on the specified page
        >>> page_util = PageUtil([1, 2, 3, 4], 1)
        >>> page_util.get_page(1)
        [1]

        """
        if not isinstance(page_number, int):
            raise TypeError("page_number must be an integer")
        if page_number < 1 or page_number > max(self.total_pages, 1):
            return []
        start = (page_number - 1) * self.page_size
        end = start + self.page_size
        return self.data[start:end]

    def get_page_info(self, page_number):
        """
        Retrieve information about a specific page.
        :param page_number: int, the page number to fetch information about
        :return: dict, containing page information such as current page number, total pages, etc.
        >>> page_util = PageUtil([1, 2, 3, 4], 1)
        >>> page_util.get_page_info(1)
        >>> {
        >>>     "current_page": 1,
        >>>     "per_page": 1,
        >>>     "total_pages": 4,
        >>>     "total_items": 4,
        >>>     "has_previous": False,
        >>>     "has_next": True,
        >>>     "data": [1]
        >>> }

        """
        if not isinstance(page_number, int):
            raise TypeError("page_number must be an integer")
        page_data = self.get_page(page_number)
        total_pages = self.total_pages
        return {
            "current_page": page_number,
            "per_page": self.page_size,
            "total_pages": total_pages,
            "total_items": self.total_items,
            "has_previous": page_number > 1 and total_pages > 0,
            "has_next": page_number < total_pages,
            "data": page_data,
        }

    def search(self, keyword):
        """
        Search for items in the data that contain the given keyword.
        :param keyword: str, the keyword to search for
        :return: dict, containing search information such as total results and matching items
        >>> page_util = PageUtil([1, 2, 3, 4], 1)
        >>> page_util.search("1")
        >>> search_info = {
        >>>     "keyword": "1",
        >>>     "total_results": 1,
        >>>     "total_pages": 1,
        >>>     "results": [1]
        >>> }
        """
        if keyword is None:
            keyword = ""
        keyword_str = str(keyword)
        results = [item for item in self.data if keyword_str in str(item)]
        total_results = len(results)
        total_pages = (total_results + self.page_size -
                       1) // self.page_size if total_results else 0
        return {
            "keyword": keyword_str,
            "total_results": total_results,
            "total_pages": total_pages,
            "results": results,
        }
