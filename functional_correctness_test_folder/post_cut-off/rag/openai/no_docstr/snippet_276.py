
import dataclasses
from typing import Any, Dict, Tuple

from pydantic import fields as pydantic_fields
from pydantic import BaseModel
from pydantic.dataclasses import dataclass as pydantic_dataclass


class NoDefaultsMixin:
    """
    Mixin so that we don't need to copy and paste the code to avoid filling JSON values
    with a full catalog of the default values of rarely-used fields.
    """

    @pydantic.model_serializer(mode="wrap")
    def _workaround_for_design_flaw_in_pydantic(self, nxt):
        """
        Workaround for a design flaw in Pydantic that forces users to accept
        unnecessary garbage in their serialized JSON data or to override
        poorly-documented serialization hooks repeatedly.  Automates overriding said
        poorly-documented serialization hooks for a single dataclass.
        See https://github.com/pydantic/pydantic/issues/4554 for the relevant dismissive
        comment from the devs. This comment suggests overriding :func:`dict()`, but that
        method was disabled a year later. Now you need to add a custom serializer method
        with a ``@model_serializer`` decorator.
        See the docs at
        https://docs.pydantic.dev/latest/api/functional_serializers/
        for some dubious information on how this API works.
        See comments below for important gotchas that aren't in the documentation.
        """
        # First, get the raw serialized dict from the next serializer
        raw: Dict[str, Any] = nxt()

        # Determine the set of fields that should always be kept
        keep_fields = set(self._keep_these_fields())

        # Helper to get the default value for a field
        def get_default(field_name: str):
            # Pydantic BaseModel
            if isinstance(self, BaseModel):
                field = self.__fields__.get(field_name)
                if field is None:
                    return None
                # If no default is set, pydantic uses Undefined
                if field.default is pydantic_fields.Undefined:
                    return None
                return field.default

            # Pydantic dataclass
            if hasattr(self, "__dataclass_fields__"):
                field = self.__dataclass_fields__.get(field_name)
                if field is None:
                    return None
                if field.default is dataclasses.MISSING:
                    return None
                return field.default

            # Regular dataclass
            if hasattr(self, "__dataclass_fields__"):
                field = self.__dataclass_fields__.get(field_name)
                if field is None:
                    return None
                if field.default is dataclasses.MISSING:
                    return None
                return field.default

            # Fallback: no default
            return None

        # Build the filtered dict
        filtered: Dict[str, Any] = {}
        for key, value in raw.items():
            if key in keep_fields:
                filtered[key] = value
                continue

            default = get_default(key)
            # If default is None and value is None, skip unless keep_fields
            if default is not None and value == default:
                continue
            # If default is None but value is None, we keep it (it might be intentional)
            filtered[key] = value

        return filtered

    def _keep_these_fields(self) -> Tuple[str, ...]:
        """
        Dataclasses that include this mixin can override this method to add specific
        default values to serialized JSON.
        This is necessary for round-tripping to JSON when there are fields that
        determine which dataclass to use for deserialization.
        """
        return ()
