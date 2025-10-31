from typing import Dict, List, Optional
from pip_api._vendor.packaging.version import parse
import pip_api

class Distribution:

    def __init__(self, name: str, version: str, location: Optional[str]=None, editable_project_location: Optional[str]=None):
        self.name = name
        self.version = parse(version)
        self.location = location
        self.editable_project_location = editable_project_location
        if pip_api.PIP_VERSION >= parse('21.3'):
            self.editable = bool(self.editable_project_location)
        else:
            self.editable = bool(self.location)

    def __repr__(self):
        return "<Distribution(name='{}', version='{}'{}{})>".format(self.name, self.version, ", location='{}'".format(self.location) if self.location else '', ", editable_project_location='{}'".format(self.editable_project_location) if self.editable_project_location else '')