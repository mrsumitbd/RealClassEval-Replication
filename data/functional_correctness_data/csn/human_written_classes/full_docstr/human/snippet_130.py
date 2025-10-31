import logging
import ldap.filter
import ldap

class _LDAPConfig:
    """
    A private class that loads and caches some global objects.
    """
    logger = None
    _ldap_configured = False

    @classmethod
    def get_ldap(cls, global_options=None):
        """
        Returns the configured ldap module.
        """
        if not cls._ldap_configured and global_options is not None:
            for opt, value in global_options.items():
                ldap.set_option(opt, value)
            cls._ldap_configured = True
        return ldap

    @classmethod
    def get_logger(cls):
        """
        Initializes and returns our logger instance.
        """
        if cls.logger is None:
            cls.logger = logging.getLogger('django_auth_ldap')
            cls.logger.addHandler(logging.NullHandler())
        return cls.logger