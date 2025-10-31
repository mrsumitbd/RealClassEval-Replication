class _MethodDocDescriptor:

    def __init__(self, session_weakref, class_name, name):
        '''Initialize the descriptor.'''
        self._session_ref = session_weakref
        self.class_name = class_name
        self.name = name

    def __get__(self, instance, owner=None):
        '''Get the documentation.'''
        doc = None
        session = self._session_ref() if self._session_ref is not None else None

        # Try session-provided documentation
        if session is not None:
            try:
                if hasattr(session, 'get_method_doc'):
                    doc = session.get_method_doc(self.class_name, self.name)
                elif hasattr(session, 'get_documentation'):
                    doc = session.get_documentation(self.class_name, self.name)
                elif hasattr(session, 'method_documentation'):
                    md = session.method_documentation
                    if isinstance(md, dict):
                        # Try various common layouts
                        doc = (
                            md.get((self.class_name, self.name)) or
                            (md.get(self.class_name, {}).get(self.name) if isinstance(md.get(self.class_name), dict) else None) or
                            md.get(self.name)
                        )
            except Exception:
                pass

        # Fallback: use the callable's __doc__ from the owner
        if doc is None:
            if owner is None and instance is not None:
                owner = instance.__class__
            target = None
            if owner is not None:
                target = getattr(owner, self.name, None)
            elif instance is not None:
                target = getattr(instance, self.name, None)
            if target is not None:
                doc = getattr(target, '__doc__', None)

        return doc or ''
