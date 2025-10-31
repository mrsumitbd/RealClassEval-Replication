class _MethodDocDescriptor:

    def __init__(self, session_weakref, class_name, name):
        self._session_weakref = session_weakref
        self._class_name = class_name
        self._name = name

    def __get__(self, instance, owner=None):
        def _compute_doc():
            session = None
            try:
                session = self._session_weakref() if callable(self._session_weakref) else None
            except Exception:
                session = None
            doc = None
            if session is not None and hasattr(session, 'get_doc'):
                try:
                    doc = session.get_doc(self._class_name, self._name)
                except Exception:
                    doc = None
            if not doc:
                doc = f"{self._class_name}.{self._name}"
            return doc

        if instance is None:
            def _unbound(*args, **kwargs):
                raise AttributeError(
                    f"'{self._class_name}' method '{self._name}' is not callable from the class.")
            _unbound.__name__ = self._name
            _unbound.__qualname__ = f"{self._class_name}.{self._name}"
            _unbound.__doc__ = _compute_doc()
            return _unbound

        impl_name = f"_{self._name}"
        impl = getattr(instance, impl_name, None)
        if impl is None and owner is not None:
            impl = getattr(owner, impl_name, None)
            if impl is not None and hasattr(impl, "__get__"):
                impl = impl.__get__(instance, owner)

        if impl is None or not callable(impl):
            def _missing(*args, **kwargs):
                raise NotImplementedError(
                    f"No implementation found for method '{self._name}'. Expected '{impl_name}'.")
            _missing.__name__ = self._name
            _missing.__qualname__ = f"{type(instance).__name__}.{self._name}"
            _missing.__doc__ = _compute_doc()
            return _missing

        # Try to enrich doc if missing
        try:
            if not getattr(impl, "__doc__", None):
                try:
                    impl.__doc__ = _compute_doc()
                except Exception:
                    pass
        except Exception:
            pass

        return impl
