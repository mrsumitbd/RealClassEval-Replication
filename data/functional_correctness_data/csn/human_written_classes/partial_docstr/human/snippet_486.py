class EmbeddedHolder:
    """Hold details of embedded content from processing a view"""

    def __init__(self):
        self.css = ''
        self.config = ''
        self.scripts = ''

    def add_css(self, css):
        """Add css content"""
        if css:
            self.css = css

    def add_config(self, config):
        """Add config content"""
        if config:
            self.config = config

    def add_scripts(self, scripts):
        """Add js content"""
        if scripts:
            self.scripts += scripts