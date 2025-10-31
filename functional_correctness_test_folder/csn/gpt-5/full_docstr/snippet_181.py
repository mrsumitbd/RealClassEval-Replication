class BaseLoader:
    '''Base class for File Loaders'''

    _EXT_TYPE_MAP = {
        'rq': 'query',
        'ru': 'update',
    }

    def getTextForName(self, query_name):
        '''Return the query text and query type for the given query name.
        Note that file extention is not part of the query name. For example,
        for `query_name='query1'` would return the content of file `query1.rq`
        from the loader's source (assuming such file exists).'''
        if not query_name or not isinstance(query_name, str):
            raise ValueError("query_name must be a non-empty string")

        # Try preferred known extensions first
        for ext, qtype in (('rq', 'query'), ('ru', 'update')):
            full = f"{query_name}.{ext}"
            text = self._getText(full)
            if text is not None:
                return text, qtype

        # Fallback: search via available files from the source
        try:
            files = self.fetchFiles()
        except NotImplementedError:
            files = None

        if files:
            prefix = f"{query_name}."
            candidates = [f for f in files if isinstance(
                f, str) and f.startswith(prefix)]
            if candidates:
                # Prefer known extensions deterministically, else choose lexicographically
                known = [f for f in candidates if f.rsplit(
                    '.', 1)[-1] in self._EXT_TYPE_MAP]
                chosen = None
                if known:
                    # Prefer rq then ru if present
                    prioritized = [f"{query_name}.rq", f"{query_name}.ru"]
                    for p in prioritized:
                        if p in known:
                            chosen = p
                            break
                    if chosen is None:
                        chosen = sorted(known)[0]
                else:
                    chosen = sorted(candidates)[0]

                text = self._getText(chosen)
                if text is not None:
                    ext = chosen.rsplit('.', 1)[-1]
                    qtype = self._EXT_TYPE_MAP.get(ext, ext)
                    return text, qtype

        raise FileNotFoundError(
            f"No file found for query name '{query_name}' with known or available extensions")

    def _getText(self, queryFullName):
        '''To be implemented by sub-classes.
        Returns None if the file does not exist.'''
        raise NotImplementedError

    def fetchFiles(self):
        '''To be implemented by sub-classes'''
        raise NotImplementedError
