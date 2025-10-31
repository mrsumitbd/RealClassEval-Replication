import time
import yaml

class FileManager:

    def __init__(self, delta=1.0):
        self._cache = {}
        self._delta = max(0.0, delta)

    def clear(self):
        self._cache.clear()

    def read_yaml(self, filename: str):
        content = None
        try:
            content = self.read(filename)
        except PermissionError:
            log.debug('PermissionError while reading %s.', filename)
        except FileNotFoundError:
            log.debug('File %s does not exists.', filename)
        except UnicodeDecodeError:
            log.debug('Encoding error %s (we assume is utf-8).', filename)
        if content is not None:
            try:
                content = yaml.safe_load(content)
            except yaml.YAMLError:
                log.debug('YAMLError reading %s.', filename)
                content = None
        return content

    def read(self, filename: str) -> str:
        if filename not in self._cache or self._cache[filename]['time'] + self._delta < time.monotonic():
            with open(filename, mode='r', encoding='utf-8') as fd:
                self._cache[filename] = {'time': time.monotonic(), 'content': fd.read()}
        return self._cache[filename]['content']