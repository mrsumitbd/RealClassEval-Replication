class SearchContextManager:
    """Context manager for search operations."""
    _instance = None

    def __init__(self):
        self.context = None
        self.previous_context = None

    def __enter__(self):
        if SearchContextManager._instance is None:
            SearchContextManager._instance = SearchContext()
        self.context = SearchContextManager._instance
        self.previous_context = get_search_context()
        set_search_context(self.context)
        return self.context

    def __exit__(self, exc_type, exc_val, exc_tb):
        set_search_context(self.previous_context)
        if self.previous_context is None:
            SearchContextManager._instance = None
        return False