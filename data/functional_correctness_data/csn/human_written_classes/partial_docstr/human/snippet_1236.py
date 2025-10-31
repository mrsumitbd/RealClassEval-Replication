class BaseValidator:

    def validate(self, value):
        """Validate value.
        :param value: value to validate
        :return None
        :raise ValidationError
        """
        pass

    def __call__(self, value):
        self.validate(value)