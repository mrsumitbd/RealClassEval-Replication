class MultiprocessingStringIO:
    def __init__(self):
        self._parts = []

    def getvalue(self):
        return ''.join(self._parts)

    def _write_from(self, content_list):
        if content_list is None:
            return
        if isinstance(content_list, (str, bytes)):
            self._parts.append(content_list if isinstance(
                content_list, str) else content_list.decode())
            return
        for item in content_list:
            if item is None:
                continue
            self._parts.append(item if isinstance(item, str) else str(item))

    def writelines(self, content_list):
        self._write_from(content_list)

    def writelines(self, content_list):
        self._write_from(content_list)
