
import copy


class Aspect:
    '''A network, ansible_host, system, deploy, configure or contextualize element in a RADL.'''

    def __init__(self, id=None):
        self.id = id

    def getId(self):
        return self.id

    def clone(self):
        '''Return a copy of this aspect.'''
        return copy.deepcopy(self)
