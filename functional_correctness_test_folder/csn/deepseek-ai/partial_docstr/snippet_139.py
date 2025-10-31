
class LazyField:

    def __init__(self, klass: 'Type[Field[Any, Any]]') -> None:
        self.klass = klass
        self.args = ()
        self.kwargs = {}

    def __call__(self, *args: Any, **kwargs: Any) -> 'LazyField':
        '''Instantiate a new field with options'''
        self.args = args
        self.kwargs = kwargs
        return self

    def update(self, **kwargs: Any) -> 'LazyField':
        '''Customize the lazy field'''
        self.kwargs.update(kwargs)
        return self

    def create(self) -> 'Field[Any, Any]':
        return self.klass(*self.args, **self.kwargs)
