from apidoc.object.source_raw import Object as ObjectRaw
from apidoc.object.source_raw import Constraintable

class Object:

    @classmethod
    def factory(cls, object_raw):
        """Return a proper object
        """
        if object_raw is None:
            return None
        if object_raw.type is ObjectRaw.Types.object:
            return ObjectObject(object_raw)
        elif object_raw.type is ObjectRaw.Types.type:
            return ObjectType(object_raw)
        elif object_raw.type is ObjectRaw.Types.array:
            return ObjectArray(object_raw)
        elif object_raw.type is ObjectRaw.Types.dynamic:
            return ObjectDynamic(object_raw)
        elif object_raw.type is ObjectRaw.Types.const:
            return ObjectConst(object_raw)
        elif object_raw.type is ObjectRaw.Types.enum:
            return ObjectEnum(object_raw)
        else:
            return Object(object_raw)

    def __init__(self, object_raw):
        self.name = object_raw.name
        self.type = object_raw.type
        self.optional = object_raw.optional
        self.sample = object_raw.get_sample()
        if isinstance(object_raw, Constraintable):
            self.constraints = object_raw.constraints
        else:
            self.constraints = {}