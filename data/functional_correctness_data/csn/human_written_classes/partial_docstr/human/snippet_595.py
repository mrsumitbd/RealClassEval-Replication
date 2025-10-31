class LDAPGroupType:
    """
    This is an abstract base class for classes that determine LDAP group
    membership. A group can mean many different things in LDAP, so we will need
    a concrete subclass for each grouping mechanism. Clients may subclass this
    if they have a group mechanism that is not handled by a built-in
    implementation.

    name_attr is the name of the LDAP attribute from which we will take the
    Django group name.

    Subclasses in this file must use self.ldap to access the python-ldap module.
    This will be a mock object during unit tests.
    """

    def __init__(self, name_attr='cn'):
        self.name_attr = name_attr
        self.ldap = _LDAPConfig.get_ldap()

    def user_groups(self, ldap_user, group_search):
        """
        Returns a list of group_info structures, each one a group to which
        ldap_user belongs. group_search is an LDAPSearch object that returns all
        of the groups that the user might belong to. Typical implementations
        will apply additional filters to group_search and return the results of
        the search. ldap_user represents the user and has the following three
        properties:

        dn: the distinguished name
        attrs: a dictionary of LDAP attributes (with lists of values)
        connection: an LDAPObject that has been bound with credentials

        This is the primitive method in the API and must be implemented.
        """
        return []

    def is_member(self, ldap_user, group_dn):
        """
        This method is an optimization for determining group membership without
        loading all of the user's groups. Subclasses that are able to do this
        may return True or False. ldap_user is as above. group_dn is the
        distinguished name of the group in question.

        The base implementation returns None, which means we don't have enough
        information. The caller will have to call user_groups() instead and look
        for group_dn in the results.
        """
        return None

    def group_name_from_info(self, group_info):
        """
        Given the (DN, attrs) 2-tuple of an LDAP group, this returns the name of
        the Django group. This may return None to indicate that a particular
        LDAP group has no corresponding Django group.

        The base implementation returns the value of the cn attribute, or
        whichever attribute was given to __init__ in the name_attr
        parameter.
        """
        try:
            name = group_info[1][self.name_attr][0]
        except (KeyError, IndexError):
            name = None
        return name