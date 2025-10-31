class SystemFieldContext:
    '''Base class for a system field context.
    A system field context is created once you access a field's attribute on
    a class. As the system field may be defined on a super class, this context
    allows us to know from which class the field was accessed.
    Normally you should subclass this class, and implement methods the methods
    on it that requires you to know the record class.
        '''

    def __init__(self, field, record_cls):
        self._field = field
        self._record_cls = record_cls

    @property
    def field(self):
        return self._field

    @property
    def record_cls(self):
        '''Record class to prevent it from being overwritten.'''
        return self._record_cls
