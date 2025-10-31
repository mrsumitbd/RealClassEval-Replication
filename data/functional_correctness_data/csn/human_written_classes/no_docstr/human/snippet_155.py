class _NullToken:

    def __bool__(self):
        return False

    def __str__(self):
        return ''