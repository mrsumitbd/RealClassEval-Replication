class GetterNameFactory:

    @staticmethod
    def get_name(validator_name: str) -> str:
        return 'get_%s' % validator_name if validator_name else 'get'

    @staticmethod
    def get_list_of_name(validator_name: str) -> str:
        return 'get_list_of_%s' % validator_name