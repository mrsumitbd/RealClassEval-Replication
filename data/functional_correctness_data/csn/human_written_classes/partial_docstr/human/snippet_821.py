class ValidationObject:
    validator_fail_msg = ''
    expected_type = None

    def __init__(self, split_func=None):
        if split_func is None:
            self.split_func = lambda x: [x]
        else:
            self.split_func = split_func

    def validator_func(self, input_value):
        """
        validator_func(self, input_value)

        Function that should validate the result of a given input value
        """
        raise NotImplementedError

    def validate(self, input_name, input_value):
        if self.expected_type is not None:
            type_result = self.validate_type(input_name, input_value)
            if not type_result[0]:
                return type_result
        for processed_value in self.split_func(input_value):
            validator_result = self.validator_func(processed_value)
            if not validator_result:
                return (False, [self.validator_fail_msg.format(input_name)])
        return (True, None)

    def validate_type(self, input_name, input_value):
        if not isinstance(input_value, self.expected_type):
            expected_type_fmt = 'Attribute {} should be instance of type {}'
            return (False, [expected_type_fmt.format(input_name, self.expected_type.__name__)])
        else:
            return (True, None)