
import copy


class Aspect:
    '''A network, ansible_host, system, deploy, configure or contextualize element in a RADL.'''

    def __init__(self, id, **kwargs):
        self.id = id
        for key, value in kwargs.items():
            setattr(self, key, value)

    def getId(self):
        return self.id

    def clone(self):
        '''Return a copy of this aspect.'''
        return copy.deepcopy(self)
