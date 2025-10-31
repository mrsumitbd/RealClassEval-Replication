
import pydantic
from pydantic import fields as pydantic_fields


class NoDefaultsMixin:
    """
    Mixin that serializes only the fields that have no default value.
    """

    @pydantic.model_serializer(mode="wrap")
    def _workaround_for_design_flaw_in_pydantic(self, nxt):
        """
        Wrap the default serializer to keep only the fields returned by
        `_keep_these_fields`.
        """
        # Get the default serialized representation
        data = nxt(self)

        # Determine which keys to keep
        keep = set(self._keep_these_fields())

        # Filter the data to include only the desired keys
        return {k: v for k, v in data.items() if k in keep}

    def _keep_these_fields(self) -> tuple[str]:
        """
        Return a tuple of field names that have no default value.
        Works with both Pydantic v1 and v2.
        """
        # Pydantic v2 uses `model_fields`, v1 uses `__fields__`
        fields = getattr(self, "model_fields", getattr(self, "__fields__", {}))

        # Collect names of fields whose default is Undefined
        return tuple(
            name
            for name, field in fields.items()
            if field.default is pydantic_fields.Undefined
        )
