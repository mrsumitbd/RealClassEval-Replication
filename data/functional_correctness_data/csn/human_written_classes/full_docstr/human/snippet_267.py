from django.db import transaction

class AtomicMixin:
    """Mixin to provide atomic transaction for as_view."""

    @classmethod
    def create_atomic_wrapper(cls, wrapped_func):
        """Returns a wrapped function."""

        def _create_atomic_wrapper(*args, **kwargs):
            """Actual wrapper."""
            with transaction.atomic():
                return wrapped_func(*args, **kwargs)
        return _create_atomic_wrapper

    @classmethod
    def as_view(cls, **initkwargs):
        """Overrides as_view to add atomic transaction."""
        view = super().as_view(**initkwargs)
        return cls.create_atomic_wrapper(view)