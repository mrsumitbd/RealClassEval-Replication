
class BaseLoader:

    def getTextForName(self, query_name):
        # Implementation of getTextForName
        queryFullName = self._getFullName(query_name)
        return self._getText(queryFullName)

    def _getText(self, queryFullName):
        # Implementation of _getText
        # This is a placeholder for fetching text based on the full name
        return f"Text for {queryFullName}"

    def fetchFiles(self):
        # Implementation of fetchFiles
        # This is a placeholder for fetching files
        return ["file1.txt", "file2.txt"]

    def _getFullName(self, query_name):
        # Helper method to construct full name
        # This is a placeholder for constructing the full name
        return f"full_{query_name}"
