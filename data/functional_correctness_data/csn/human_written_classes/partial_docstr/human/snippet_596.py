class LDAPSearchUnion:
    """
    A compound search object that returns the union of the results. Instantiate
    it with one or more LDAPSearch objects.
    """

    def __init__(self, *args):
        self.searches = args
        self.ldap = _LDAPConfig.get_ldap()

    def search_with_additional_terms(self, term_dict, escape=True):
        searches = [s.search_with_additional_terms(term_dict, escape) for s in self.searches]
        return type(self)(*searches)

    def search_with_additional_term_string(self, filterstr):
        searches = [s.search_with_additional_term_string(filterstr) for s in self.searches]
        return type(self)(*searches)

    def execute(self, connection, filterargs=(), escape=True):
        msgids = [search._begin(connection, filterargs, escape) for search in self.searches]
        results = {}
        for search, msgid in zip(self.searches, msgids):
            if msgid is not None:
                result = search._results(connection, msgid)
                results.update(dict(result))
        return results.items()