
class BaseLoader:

    def getTextForName(self, query_name):
        query_full_name = self._prepare_query_name(query_name)
        return self._getText(query_full_name)

    def _getText(self, queryFullName):
        raise NotImplementedError("Subclasses must implement this method")

    def fetchFiles(self):
        raise NotImplementedError("Subclasses must implement this method")

    def _prepare_query_name(self, query_name):
        return query_name.strip().lower()
