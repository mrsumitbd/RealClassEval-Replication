class JavaField:
    """
    Represents a field in a Java class description
    """

    def __init__(self, field_type, name, class_name=None):
        self.type = field_type
        self.name = name
        self.class_name = class_name
        self.is_inner_class_reference = False
        if self.class_name:
            self.validate(self.class_name.value)

    def validate(self, java_type):
        """
        Validates the type given as parameter
        """
        if self.type == FieldType.OBJECT:
            if not java_type:
                raise ValueError("Class name can't be empty")
            if java_type[0] != 'L' or java_type[-1] != ';':
                raise ValueError('Invalid object field type: {0}'.format(java_type))