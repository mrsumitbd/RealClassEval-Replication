class AbstractStateBackend:

    @staticmethod
    def from_bool_to_str_value(value):
        value = str(int(value))
        if value not in ['0', '1']:
            raise ValueError('state value is not 0|1')
        return value

    @staticmethod
    def from_str_to_bool_value(value):
        value = value.strip()
        if value not in ['0', '1']:
            raise ValueError('state value is not 0|1')
        value = bool(int(value))
        return value

    def get_value(self):
        raise NotImplementedError()

    def set_value(self, value):
        raise NotImplementedError()