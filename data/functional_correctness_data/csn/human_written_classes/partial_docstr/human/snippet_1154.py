class HerokuConnectFieldMixin:
    """Base mixin for Heroku Connect fields."""
    sf_field_name = None
    upsert = False

    def __init__(self, *args, **kwargs):
        self.sf_field_name = kwargs.pop('sf_field_name')
        kwargs.setdefault('db_column', self.sf_field_name.lower())
        kwargs.setdefault('null', True)
        self.upsert = kwargs.pop('upsert', False)
        if self.upsert:
            kwargs.update({'unique': True, 'db_index': True})
        super().__init__(*args, **kwargs)
        if self.unique:
            self.db_index = True

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['sf_field_name'] = self.sf_field_name
        kwargs['upsert'] = self.upsert
        return (name, path, args, kwargs)