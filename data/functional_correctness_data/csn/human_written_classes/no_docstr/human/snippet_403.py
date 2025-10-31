import inspect

class Boxed:

    def __init__(self, name=None):
        self.name = name

    def __set_name__(self, owner, name):
        if not self.name:
            self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.name).value

    def __set__(self, instance, value):
        if not hasattr(instance, self.name):
            if isinstance(value, Box):
                setattr(instance, self.name, value)
            elif inspect.isdatadescriptor(value):
                default = getattr(value, 'default', None)
                if default is not None:
                    setattr(instance, self.name, Box(default))
                    return
                if hasattr(value, '__get__'):
                    try:
                        default = value.__get__(instance, owner=type(instance))
                        if default:
                            setattr(instance, self.name, Box(default))
                            return
                    except Exception:
                        pass
                raise TypeError(f"__init__() missing required argument to be stored as: '{value.name}'or cannot find default value for descriptor: {value} (default should be provided either by 'default' attribute or by __get__ method)")
            else:
                setattr(instance, self.name, Box(value))
        else:
            getattr(instance, self.name).value = value