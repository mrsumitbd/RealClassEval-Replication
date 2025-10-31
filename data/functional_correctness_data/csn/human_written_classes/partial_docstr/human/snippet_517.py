class shared_parameters:
    """
    Context manager to share parameter instances when creating
    multiple Parameterized objects of the same type. Parameter default
    values are instantiated once and cached to be reused when another
    Parameterized object of the same type is instantiated.
    Can be useful to easily modify large collections of Parameterized
    objects at once and can provide a significant speedup.
    """
    _share = False
    _shared_cache = {}

    def __enter__(self):
        shared_parameters._share = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        shared_parameters._share = False
        shared_parameters._shared_cache = {}