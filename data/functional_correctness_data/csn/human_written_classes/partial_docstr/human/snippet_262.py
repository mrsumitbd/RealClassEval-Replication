import re
import sys

class attriObject:
    """Class object for attribute parser."""

    def __init__(self, string):
        self.value = re.split(':', string)
        self.title = self.value[-1]

    def getElement(self, json_object):
        found = [json_object]
        for entry in self.value:
            for index in range(len(found)):
                try:
                    found[index] = found[index][entry]
                except (TypeError, KeyError):
                    print("'{0}' is not a valid json entry.".format(':'.join(self.value)))
                    sys.exit()
                if isinstance(found[index], list):
                    if len(found) > 1:
                        raise Exception('Extractor currently does not handle nested lists.')
                    found = found[index]
        return found