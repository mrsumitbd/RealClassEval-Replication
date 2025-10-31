
class LazyField:
    '''A Field that can be later customized until it is binded to the final Model'''

    def __init__(self, klass: 'Type[Field[Any, Any]]') -> None:
        '''Instantiate the field type'''
        self.klass = klass
        self.args = ()
        self.kwargs = {}

    def __call__(self, *args: Any, **kwargs: Any) -> 'LazyField':
        '''Instantiate a new field with options'''
        new_field = LazyField(self.klass)
        new_field.args = args
        new_field.kwargs = kwargs
        return new_field

    def update(self, **kwargs: Any) -> 'LazyField':
        '''Customize the lazy field'''
        new_field = LazyField(self.klass)
        new_field.args = self.args
        new_field.kwargs = {**self.kwargs, **kwargs}
        return new_field

    def create(self) -> 'Field[Any, Any]':
        '''Create a normal field from the lazy field'''
        return self.klass(*self.args, **self.kwargs)
