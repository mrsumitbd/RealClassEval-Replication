
class Aspect:
    '''A network, ansible_host, system, deploy, configure or contextualize element in a RADL.'''

    def getId(self):
        '''Return the id of the aspect.'''
        pass

    def clone(self):
        '''Return a copy of this aspect.'''
        pass
