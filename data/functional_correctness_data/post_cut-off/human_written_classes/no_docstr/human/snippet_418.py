class InputResolver:

    def __init__(self, input_instance, is_encode_binary: bool=True, custom_type_resolver: dict={}):
        self._instance = input_instance
        self._is_encode_binary = is_encode_binary
        self._custom_type_resolver = custom_type_resolver

    def __next__(self):
        while True:
            return resolve_input(self._instance, self._is_encode_binary, self._custom_type_resolver)

    def __iter__(self):
        return self