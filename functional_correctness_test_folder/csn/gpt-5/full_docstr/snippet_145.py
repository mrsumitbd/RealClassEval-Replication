class _MethodDocDescriptor:
    '''An object that dynamically fetches the documentation
    for an Octave user class method.
        '''

    def __init__(self, session_weakref, class_name, name):
        '''Initialize the descriptor.'''
        self._session_ref = session_weakref
        self._class_name = class_name
        self._name = name
        self._doc_cache = None

    def __get__(self, instance, owner=None):
        '''Get the documentation.'''
        if self._doc_cache is not None:
            return self._doc_cache

        session = self._session_ref() if self._session_ref is not None else None
        doc = None

        # Try to ask the session for the documentation via several possible methods.
        if session is not None:
            candidates = [
                ("get_class_method_doc", (self._class_name, self._name), {}),
                ("get_method_doc", (self._class_name, self._name), {}),
                ("get_octave_method_doc", (self._class_name, self._name), {}),
                ("get_doc", (f"{self._class_name}.{self._name}",), {}),
                ("get_doc", (self._name,), {}),
            ]
            for meth_name, args, kwargs in candidates:
                try:
                    meth = getattr(session, meth_name, None)
                    if callable(meth):
                        result = meth(*args, **kwargs)
                        if result:
                            doc = str(result)
                            break
                except Exception:
                    # Ignore and try next candidate
                    pass

        # Fallback: try Python attribute doc if accessible
        if not doc:
            try:
                target = None
                if instance is not None:
                    target = getattr(instance, self._name, None)
                elif owner is not None:
                    target = getattr(owner, self._name, None)
                if target is not None:
                    doc_attr = getattr(target, "__doc__", None)
                    if doc_attr:
                        doc = str(doc_attr)
            except Exception:
                pass

        if doc is None:
            doc = ""

        self._doc_cache = doc
        return self._doc_cache
