from indico_piwik.piwik import PiwikRequest

class PiwikQueryBase:
    """Base Piwik query"""

    def __init__(self, query_script):
        from indico_piwik.plugin import PiwikPlugin
        self.request = PiwikRequest(server_url=PiwikPlugin.settings.get('server_api_url'), site_id=PiwikPlugin.settings.get('site_id_events'), api_token=PiwikPlugin.settings.get('server_token'), query_script=query_script)

    def call(self, **query_params):
        return self.request.call(**query_params)