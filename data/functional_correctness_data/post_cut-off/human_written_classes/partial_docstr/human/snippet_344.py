class SimBrowser:
    """Simulated browser for rendering the HTML source of WebShop environment pages."""

    def __init__(self, server):
        self.server = server
        self.current_url = None
        self.page_source = None
        self.session_id = None

    def get(self, url, session_id=None, session_int=None):
        """Set browser variables to corresponding link, page HTML for URL"""
        self.session_id = url.split('/')[-1] if session_id is None else session_id
        self.page_source, _, _ = self.server.receive(self.session_id, self.current_url, session_int=session_int)
        self.current_url = url

    def click(self, clickable_name, text_to_clickable):
        """Wrapper for `receive` handler for performing click action on current page"""
        self.page_source, self.current_url, status = self.server.receive(self.session_id, current_url=self.current_url, clickable_name=clickable_name, text_to_clickable=text_to_clickable)
        return status

    def search(self, keywords):
        """Wrapper for `receive` handler for performing search action on current page"""
        if isinstance(keywords, str):
            keywords = keywords.split(' ')
        self.page_source, self.current_url, status = self.server.receive(self.session_id, current_url=self.current_url, keywords=keywords)
        return status