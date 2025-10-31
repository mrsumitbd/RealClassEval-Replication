class RFC7033Webfinger:
    """
    RFC 7033 webfinger - see https://tools.ietf.org/html/rfc7033

    A Django view is also available, see the child ``django`` module for view and url configuration.

    :param id: Profile ActivityPub ID in URL format
    :param handle: Profile Diaspora handle
    :param guid: Profile Diaspora guid
    :param base_url: The base URL of the server (protocol://domain.tld)
    :param profile_path: Profile path for the user (for example `/profile/johndoe/`)
    :param hcard_path: (Optional) hCard path, defaults to ``/hcard/users/``.
    :param atom_path: (Optional) atom feed path
    :returns: dict
    """

    def __init__(self, id: str, handle: str, guid: str, base_url: str, profile_path: str, hcard_path: str='/hcard/users/', atom_path: str=None, search_path: str=None):
        self.id = id
        self.handle = handle
        self.guid = guid
        self.base_url = base_url
        self.hcard_path = hcard_path
        self.profile_path = profile_path
        self.atom_path = atom_path
        self.search_path = search_path

    def render(self):
        webfinger = {'subject': 'acct:%s' % self.handle, 'aliases': [f'{self.base_url}{self.profile_path}', self.id], 'links': [{'rel': 'http://microformats.org/profile/hcard', 'type': 'text/html', 'href': '%s%s%s' % (self.base_url, self.hcard_path, self.guid)}, {'rel': 'http://joindiaspora.com/seed_location', 'type': 'text/html', 'href': self.base_url}, {'rel': 'http://webfinger.net/rel/profile-page', 'type': 'text/html', 'href': '%s%s' % (self.base_url, self.profile_path)}, {'rel': 'salmon', 'href': '%s/receive/users/%s' % (self.base_url, self.guid)}]}
        webfinger['links'].append({'rel': 'self', 'href': self.id, 'type': 'application/activity+json'})
        if self.atom_path:
            webfinger['links'].append({'rel': 'http://schemas.google.com/g/2010#updates-from', 'type': 'application/atom+xml', 'href': '%s%s' % (self.base_url, self.atom_path)})
        if self.search_path:
            webfinger['links'].append({'rel': 'http://ostatus.org/schema/1.0/subscribe', 'template': '%s%s{uri}' % (self.base_url, self.search_path)})
        return webfinger