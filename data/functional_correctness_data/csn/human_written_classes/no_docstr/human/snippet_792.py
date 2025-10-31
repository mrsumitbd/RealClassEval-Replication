class ReaderNameFactory:

    @staticmethod
    def get_name(name: str) -> str:
        return 'read_%s' % name if name else 'read'

    @staticmethod
    def get_list_of_name(name: str) -> str:
        return 'read_list_of_%s' % name