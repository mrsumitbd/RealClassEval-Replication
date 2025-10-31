import pickle
import _jpype

class JUnpickler(pickle.Unpickler):
    """Unpickler overloaded to support Java objects

    Parameters:
        file: a file or other readable object.
        *args: any arguments support by the native unpickler.

    Raises:
        java.lang.ClassNotFoundException: if a serialized class is not
            found by the current classloader.
        java.io.InvalidClassException: if the serialVersionUID for the
            class does not match, usually as a result of a new jar
            version.
        java.io.StreamCorruptedException: if the pickle file has been
            altered or corrupted.

    """

    def __init__(self, file, *args, **kwargs):
        self._decoder = _jpype.JClass('org.jpype.pickle.Decoder')()
        pickle.Unpickler.__init__(self, file, *args, **kwargs)

    def find_class(self, module, cls):
        """Specialization for Java classes.

        We just need to substitute the stub class for a real
        one which points to our decoder instance.
        """
        if cls == 'JUnserializer':
            decoder = self._decoder

            class JUnserializer(object):

                def __call__(self, *args):
                    return decoder.unpack(args[0])
            return JUnserializer
        return pickle.Unpickler.find_class(self, module, cls)