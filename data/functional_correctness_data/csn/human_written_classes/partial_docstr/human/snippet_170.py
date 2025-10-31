class MotorAttributeFactory:
    """Used by Motor classes to mark attributes that delegate in some way to
    PyMongo. At module import time, create_class_with_framework calls
    create_attribute() for each attr to create the final class attribute.
    """

    def __init__(self, doc=None):
        self.doc = doc

    def create_attribute(self, cls, attr_name):
        raise NotImplementedError