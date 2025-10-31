class ModelFactoryWithValidation:
    """
    A Model mixin that provides validation-based factory methods.
    """

    @classmethod
    def create_with_validation(cls, *args, **kwargs):
        """
        Factory method that creates and validates the model object before it is saved.
        """
        ret_val = cls(*args, **kwargs)
        ret_val.full_clean()
        ret_val.save()
        return ret_val

    @classmethod
    def get_or_create_with_validation(cls, *args, **kwargs):
        """
        Factory method that gets or creates-and-validates the model object before it is saved.
        Similar to the get_or_create method on Models, it returns a tuple of (object, created),
        where created is a boolean specifying whether an object was created.
        """
        try:
            return (cls.objects.get(*args, **kwargs), False)
        except cls.DoesNotExist:
            return (cls.create_with_validation(*args, **kwargs), True)