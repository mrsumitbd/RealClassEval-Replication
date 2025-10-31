from grlc.queryTypes import qType, guessQueryType
import json

class BaseLoader:
    """Base class for File Loaders"""

    def getTextForName(self, query_name):
        """Return the query text and query type for the given query name.
        Note that file extention is not part of the query name. For example,
        for `query_name='query1'` would return the content of file `query1.rq`
        from the loader's source (assuming such file exists)."""
        candidateNames = [query_name + '.rq', query_name + '.sparql', query_name + '.tpf', query_name + '.json']
        candidates = [(name, guessQueryType(name)) for name in candidateNames]
        for queryFullName, queryType in candidates:
            queryText = self._getText(queryFullName)
            if queryText:
                if queryType == qType['JSON']:
                    queryText = json.loads(queryText)
                    if 'proto' not in queryText and '@graph' not in queryText:
                        continue
                return (queryText, queryType)
        return ('', None)

    def _getText(self, queryFullName):
        """To be implemented by sub-classes.
        Returns None if the file does not exist."""
        raise NotImplementedError('Subclasses must override _getText()!')

    def fetchFiles(self):
        """To be implemented by sub-classes"""
        raise NotImplementedError('Subclasses must override fetchFiles()!')