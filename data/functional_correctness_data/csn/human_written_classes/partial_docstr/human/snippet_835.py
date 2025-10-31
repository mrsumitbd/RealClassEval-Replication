from typing import Callable, Tuple, List, Dict
from federation.types import UserType, RequestType
from federation.entities.matrix.entities import MatrixEntityMixin

class Protocol:
    actor = None
    get_contact_key = None
    payload = None
    request = None
    user = None

    @staticmethod
    def build_send(entity: MatrixEntityMixin, *args, **kwargs) -> List[Dict]:
        """
        Build POST data for sending out to the homeserver.

        :param entity: The outbound ready entity for this protocol.
        :returns: list of payloads
        """
        return entity.payloads()

    def extract_actor(self):
        pass

    def receive(self, request: RequestType, user: UserType=None, sender_key_fetcher: Callable[[str], str]=None, skip_author_verification: bool=False) -> Tuple[str, dict]:
        """
        Receive a request.

        Matrix appservices will deliver 1+ events at a time.
        """
        return (self.actor, self.payload)