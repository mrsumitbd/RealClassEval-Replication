import uuid

class IPythonDisplay:
    """Reactive display handler that updates the output."""
    enabled = True

    def __init__(self, reactive):
        self._reactive = reactive

    def __call__(self):
        from param.depends import depends
        from param.parameterized import Undefined, resolve_ref
        from param.reactive import rx
        handle = None
        if isinstance(self._reactive, rx):
            cb = self._reactive._callback

            @depends(*self._reactive._params, watch=True)
            def update_handle(*args, **kwargs):
                if handle is not None:
                    handle.update(cb())
        else:
            cb = self._reactive

            @depends(*resolve_ref(cb), watch=True)
            def update_handle(*args, **kwargs):
                if handle is not None:
                    handle.update(cb())
        try:
            obj = cb()
            if obj is Undefined:
                obj = None
            handle = display(obj, display_id=uuid.uuid4().hex)
        except TypeError:
            raise NotImplementedError