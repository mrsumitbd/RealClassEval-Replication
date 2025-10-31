import copy


class Aspect:
    '''A network, ansible_host, system, deploy, configure or contextualize element in a RADL.'''

    def __init__(self, id=None, **attributes):
        self._id = id
        self._attributes = dict(attributes)

    def getId(self):
        '''Return the id of the aspect.'''
        return self._id

    def clone(self):
        '''Return a copy of this aspect.'''
        return copy.deepcopy(self)

    def __deepcopy__(self, memo):
        new_obj = self.__class__.__new__(self.__class__)
        memo[id(self)] = new_obj
        new_obj._id = copy.deepcopy(self._id, memo)
        new_obj._attributes = copy.deepcopy(self._attributes, memo)
        return new_obj

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self._id!r}, attributes={self._attributes!r})"
