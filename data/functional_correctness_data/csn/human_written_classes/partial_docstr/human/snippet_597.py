from django.conf import settings

class LDAPSettings:
    """
    This is a simple class to take the place of the global settings object. An
    instance will contain all of our settings as attributes, with default values
    if they are not specified by the configuration.
    """
    _prefix = 'AUTH_LDAP_'
    defaults = {'ALWAYS_UPDATE_USER': True, 'AUTHORIZE_ALL_USERS': False, 'BIND_AS_AUTHENTICATING_USER': False, 'REFRESH_DN_ON_BIND': False, 'BIND_DN': '', 'BIND_PASSWORD': '', 'CONNECTION_OPTIONS': {}, 'DENY_GROUP': None, 'FIND_GROUP_PERMS': False, 'CACHE_TIMEOUT': 0, 'GROUP_SEARCH': None, 'GROUP_TYPE': None, 'MIRROR_GROUPS': None, 'MIRROR_GROUPS_EXCEPT': None, 'PERMIT_EMPTY_PASSWORD': False, 'REQUIRE_GROUP': None, 'NO_NEW_USERS': False, 'SERVER_URI': 'ldap://localhost', 'START_TLS': False, 'USER_QUERY_FIELD': None, 'USER_ATTRLIST': None, 'USER_ATTR_MAP': {}, 'USER_DN_TEMPLATE': None, 'USER_FLAGS_BY_GROUP': {}, 'USER_SEARCH': None}

    def __init__(self, prefix='AUTH_LDAP_', defaults={}):
        """
        Loads our settings from django.conf.settings, applying defaults for any
        that are omitted.
        """
        self._prefix = prefix
        defaults = dict(self.defaults, **defaults)
        for name, default in defaults.items():
            value = getattr(settings, prefix + name, default)
            setattr(self, name, value)

    def _name(self, suffix):
        return self._prefix + suffix