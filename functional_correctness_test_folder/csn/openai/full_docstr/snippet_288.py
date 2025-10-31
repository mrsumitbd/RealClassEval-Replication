
import copy


class Aspect:
    '''A network, ansible_host, system, deploy, configure or contextualize element in a RADL.'''

    def __init__(self, id=None, **kwargs):
        """
        Initialize an Aspect.

        Parameters
        ----------
        id : str, optional
            Identifier for the aspect. If not provided, it will be set to None.
        **kwargs
            Additional keyword arguments are stored as attributes on the instance.
        """
        self.id = id
        for key, value in kwargs.items():
            setattr(self, key, value)

    def getId(self):
        '''Return the id of the aspect.'''
        return self.id

    def clone(self):
        '''Return a copy of this aspect.'''
        return copy.deepcopy(self)
