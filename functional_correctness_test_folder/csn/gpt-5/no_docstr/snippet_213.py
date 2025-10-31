class BaseAuthenticationMiddleware:
    def __init__(self, user_storage=None, name=None):
        if user_storage is None:
            storages = []
        elif isinstance(user_storage, (list, tuple, set)):
            storages = list(user_storage)
        else:
            storages = [user_storage]

        self.user_storage = [s for s in storages if s is not None]
        self.name = name or "user"

    def process_resource(self, req, resp, resource, uri_kwargs=None):
        ctx = self._ensure_context(req)
        errors = self._ensure_errors(ctx)

        try:
            identity = self.identify(req, resp, resource, uri_kwargs or {})
        except Exception as exc:
            errors.append(exc)
            identity = None

        self._store_identity(ctx, identity)

    def identify(self, req, resp, resource, uri_kwargs):
        for storage in self.user_storage:
            user = self.try_storage(storage, req, resp, resource, uri_kwargs)
            if user is not None:
                return user
        return None

    def try_storage(self, identifier, req, resp, resource, uri_kwargs):
        try:
            if callable(identifier):
                return identifier(req, resp, resource, uri_kwargs)
            identify_method = getattr(identifier, "identify", None)
            if callable(identify_method):
                return identify_method(req, resp, resource, uri_kwargs)
        except Exception:
            pass
        return None

    # Internal helpers
    def _ensure_context(self, req):
        if not hasattr(req, "context") or req.context is None:
            req.context = {}
        return req.context

    def _ensure_errors(self, ctx):
        # Support both dict-like and attribute contexts
        key = f"{self.name}_auth_errors"
        if isinstance(ctx, dict):
            errors = ctx.get(key)
            if errors is None:
                errors = []
                ctx[key] = errors
            return errors
        else:
            errors = getattr(ctx, key, None)
            if errors is None:
                errors = []
                setattr(ctx, key, errors)
            return errors

    def _store_identity(self, ctx, identity):
        # Support both dict-like and attribute contexts
        if isinstance(ctx, dict):
            ctx[self.name] = identity
        else:
            setattr(ctx, self.name, identity)
