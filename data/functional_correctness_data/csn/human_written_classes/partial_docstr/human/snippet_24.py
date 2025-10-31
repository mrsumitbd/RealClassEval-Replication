import cloudpickle
import pickle

class Serializer:
    """Save data items to an input stream."""

    def __init__(self, out_stream, block_name, version):
        self.out_stream = out_stream
        self.block_name = block_name
        self.block_version = version
        self.serializer_version = 0

    def __enter__(self):
        log.debug('serializer_version = %d', self.serializer_version)
        pickle.dump(self.serializer_version, self.out_stream)
        log.debug('block_name = %s', self.block_name)
        pickle.dump(self.block_name, self.out_stream)
        log.debug('block_version = %d', self.block_version)
        pickle.dump(self.block_version, self.out_stream)
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        log.debug('END_BLOCK___')
        pickle.dump('END_BLOCK___', self.out_stream)

    def save(self, name, value, encoder='auto'):
        """Dump a data item to the current input stream."""
        log.debug('name = %s', name)
        pickle.dump(name, self.out_stream)
        if encoder is None or encoder is False:
            log.debug('encoder_name = %s', 'no_encoder')
            pickle.dump('no_encoder', self.out_stream)
        elif callable(encoder):
            log.debug('encoder_name = %s', 'custom_encoder')
            pickle.dump('custom_encoder', self.out_stream)
            encoder(value, self.out_stream)
        elif encoder == '.save' or (isinstance(value, Serializable) and encoder == 'auto'):
            if hasattr(value, 'save'):
                log.debug('encoder_name = %s', 'serializable.save')
                pickle.dump('serializable.save', self.out_stream)
                value.save(self.out_stream)
            else:
                log.debug('encoder_name = %s', 'cloudpickle.dump (fallback)')
                pickle.dump('cloudpickle.dump', self.out_stream)
                cloudpickle.dump(value, self.out_stream)
        elif encoder == 'auto':
            if isinstance(value, (int, float, str)):
                log.debug('encoder_name = %s', 'pickle.dump')
                pickle.dump('pickle.dump', self.out_stream)
                pickle.dump(value, self.out_stream)
            else:
                log.debug('encoder_name = %s', 'cloudpickle.dump')
                pickle.dump('cloudpickle.dump', self.out_stream)
                cloudpickle.dump(value, self.out_stream)
        else:
            raise ValueError(f"Unknown encoder type '{encoder}' given for serialization!")
        log.debug('value = %s', str(value))