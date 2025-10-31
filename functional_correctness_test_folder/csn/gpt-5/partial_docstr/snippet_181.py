class BaseLoader:
    '''Base class for File Loaders'''

    # Known extensions mapped to query types; subclasses may override/extend
    EXT_TO_TYPE = {
        '.rq': 'SPARQL',
        '.sparql': 'SPARQL',
        '.ru': 'SPARQL-UPDATE',
        '.sql': 'SQL',
        '.graphql': 'GRAPHQL',
        '.gql': 'GRAPHQL',
        '.cypher': 'CYPHER',
        '.cql': 'CYPHER',
        '.json': 'JSON',
        '.ndjson': 'NDJSON',
        '.yaml': 'YAML',
        '.yml': 'YAML',
        '.xml': 'XML',
        '.txt': 'TEXT',
    }

    # Extension resolution priority; subclasses can override
    EXT_PRIORITY = (
        '.rq',
        '.sparql',
        '.ru',
        '.sql',
        '.graphql',
        '.gql',
        '.cypher',
        '.cql',
        '.json',
        '.ndjson',
        '.yaml',
        '.yml',
        '.xml',
        '.txt',
    )

    def getTextForName(self, query_name):
        '''Return the query text and query type for the given query name.
        Note that file extention is not part of the query name. For example,
        for `query_name='query1'` would return the content of file `query1.rq`
        from the loader's source (assuming such file exists).'''
        if not isinstance(query_name, str) or not query_name:
            raise ValueError("query_name must be a non-empty string")

        available = self.fetchFiles()
        if available is None:
            available = []
        available_set = set(available)

        # If the name already includes an extension, use it directly if available
        dot_idx = query_name.rfind('.')
        candidates = []
        if dot_idx != -1 and dot_idx != len(query_name) - 1:
            # Has an extension
            candidates = [query_name]
        else:
            # Try with known extensions in priority order
            candidates = [f"{query_name}{ext}" for ext in self.EXT_PRIORITY]

        chosen = None
        for cand in candidates:
            if cand in available_set:
                chosen = cand
                break

        if chosen is None:
            # As a last resort, if exactly one file matches the basename regardless of extension, use it
            basename_matches = [
                fname for fname in available if fname.startswith(query_name + '.')]
            if len(basename_matches) == 1:
                chosen = basename_matches[0]

        if chosen is None:
            raise FileNotFoundError(
                f"No file found for query name '{query_name}'")

        text = self._getText(chosen)
        if not isinstance(text, str):
            raise TypeError("_getText must return a string")

        # Determine query type from extension
        ext = ''
        dot = chosen.rfind('.')
        if dot != -1:
            ext = chosen[dot:].lower()
        qtype = self.EXT_TO_TYPE.get(
            ext, ext.lstrip('.').upper() if ext else 'UNKNOWN')

        return text, qtype

    def _getText(self, queryFullName):
        raise NotImplementedError(
            "_getText must be implemented by subclasses to return file contents as string")

    def fetchFiles(self):
        raise NotImplementedError(
            "fetchFiles must be implemented by subclasses to return an iterable of available file names")
