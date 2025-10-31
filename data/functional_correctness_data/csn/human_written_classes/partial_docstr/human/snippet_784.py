from linode_api4.objects.dbase import DerivedBase
from linode_api4.objects.base import Base, Property

class Grant:
    """
    A Grant is a single grant a user has to an object.  A Grant's entity is
    an object on the account, such as a Linode, NodeBalancer, or Volume, and
    its permissions level is one of None, "read_only" or "read_write".

    Grants cannot be accessed or updated individually, and are only relevant in
    the context of a UserGrants object.
    """

    def __init__(self, client, cls, dct):
        self._client = client
        self.cls = cls
        self.id = dct['id']
        self.label = dct['label']
        self.permissions = dct['permissions']

    @property
    def entity(self):
        """
        Returns the object this grant is for.  The objects type depends on the
        type of object this grant is applied to, and the object returned is
        not populated (accessing its attributes will trigger an api request).

        :returns: This grant's entity
        :rtype: Linode, NodeBalancer, Domain, StackScript, Volume, or Longview
        """
        if not issubclass(self.cls, Base) or issubclass(self.cls, DerivedBase):
            raise ValueError('Cannot get entity for non-base-class {}'.format(self.cls))
        return self.cls(self._client, self.id)

    def _serialize(self, *args, **kwargs):
        """
        Returns this grant in as JSON the api will accept.  This is only relevant
        in the context of UserGrants.save
        """
        return {'permissions': self.permissions, 'id': self.id}