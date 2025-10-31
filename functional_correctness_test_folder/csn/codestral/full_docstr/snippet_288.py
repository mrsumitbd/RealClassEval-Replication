
class Aspect:
    '''A network, ansible_host, system, deploy, configure or contextualize element in a RADL.'''

    def __init__(self, id):
        self.id = id

    def getId(self):
        '''Return the id of the aspect.'''
        return self.id

    def clone(self):
        '''Return a copy of this aspect.'''
        return Aspect(self.id)
