import os
import json
from jsonschema import validate

class SocialRelayWellKnown:
    """A `.well-known/social-relay` document in JSON.

    For apps wanting to announce their preferences towards relay applications.

    See WIP spec: https://wiki.diasporafoundation.org/Relay_servers_for_public_posts

    Schema see `schemas/social-relay-well-known.json`

    :arg subscribe: bool
    :arg tags: tuple, optional
    :arg scope: Should be either "all" or "tags", default is "all" if not given
    """

    def __init__(self, subscribe, tags=(), scope='all', *args, **kwargs):
        self.doc = {'subscribe': subscribe, 'scope': scope, 'tags': list(tags)}

    def render(self):
        self.validate_doc()
        return json.dumps(self.doc)

    def validate_doc(self):
        schema_path = os.path.join(os.path.dirname(__file__), 'schemas', 'social-relay-well-known.json')
        with open(schema_path) as f:
            schema = json.load(f)
        validate(self.doc, schema)