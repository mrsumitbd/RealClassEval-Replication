
import copy


class Aspect:
    '''A network, ansible_host, system, deploy, configure or contextualize element in a RADL.'''

    def __init__(self, aspect_id=None):
        self._id = aspect_id

    def getId(self):
        '''Return the id of the aspect.'''
        return self._id

    def clone(self):
        '''Return a copy of this aspect.'''
        return copy.deepcopy(self)
