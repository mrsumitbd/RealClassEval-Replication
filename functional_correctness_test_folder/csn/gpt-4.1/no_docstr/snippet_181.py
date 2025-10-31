
class BaseLoader:

    def getTextForName(self, query_name):
        return self._getText(query_name)

    def _getText(self, queryFullName):
        # Placeholder: In a real implementation, this would fetch text for the given name.
        # Here, we just return a string for demonstration.
        return f"Text for {queryFullName}"

    def fetchFiles(self):
        # Placeholder: In a real implementation, this would fetch files.
        # Here, we just return an empty list.
        return []
