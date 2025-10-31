
class Aspect:
    '''A network, ansible_host, system, deploy, configure or contextualize element in a RADL.'''

    def __init__(self, aspect_id):
        self.aspect_id = aspect_id

    def getId(self):
        '''Return the id of the aspect.'''
        return self.aspect_id

    def clone(self):
        '''Return a copy of this aspect.'''
        return Aspect(self.aspect_id)
