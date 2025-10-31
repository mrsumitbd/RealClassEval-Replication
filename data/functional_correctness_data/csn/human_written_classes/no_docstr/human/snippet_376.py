class LazyImportPdb:

    def __repr__(self):
        return "<class 'pdb.Pdb'>"
    __str__ = __repr__

    def __call__(self, **kwargs):
        from pdb import Pdb
        return Pdb(**kwargs)