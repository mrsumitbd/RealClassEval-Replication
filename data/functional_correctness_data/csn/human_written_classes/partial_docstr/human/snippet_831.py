import json
import os
import warnings
from jsonschema import validate
from jsonschema.exceptions import ValidationError

class NodeInfo:
    """Generate a NodeInfo document.

    See spec: http://nodeinfo.diaspora.software

    NodeInfo is unnecessarely restrictive in field values. We wont be supporting such strictness, though
    we will raise a warning unless validation is skipped with `skip_validate=True`.

    For strictness, `raise_on_validate=True` will cause a `ValidationError` to be raised.

    See schema document `federation/hostmeta/schemas/nodeinfo-1.0.json` for how to instantiate this class.
    """

    def __init__(self, software, protocols, services, open_registrations, usage, metadata, skip_validate=False, raise_on_validate=False):
        self.doc = {'version': '1.0', 'software': software, 'protocols': protocols, 'services': services, 'openRegistrations': open_registrations, 'usage': usage, 'metadata': metadata}
        self.skip_validate = skip_validate
        self.raise_on_validate = raise_on_validate

    def render(self):
        if not self.skip_validate:
            self.validate_doc()
        return json.dumps(self.doc)

    def validate_doc(self):
        schema_path = os.path.join(os.path.dirname(__file__), 'schemas', 'nodeinfo-1.0.json')
        with open(schema_path) as f:
            schema = json.load(f)
        try:
            validate(self.doc, schema)
        except ValidationError:
            if self.raise_on_validate:
                raise
            warnings.warn('NodeInfo document generated does not validate against NodeInfo 1.0 specification.')