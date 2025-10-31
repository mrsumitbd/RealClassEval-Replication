
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class StatusBioDTO:
    """
    Status biography data transfer object.
    This DTO is intentionally dynamic – it accepts any attributes that
    are present on the source model.
    """

    # No explicit fields are declared; attributes are set dynamically in __init__.

    def __init__(self, **kwargs: Any) -> None:
        """
        Dynamically assign attributes from keyword arguments.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def from_model(cls, model: Any) -> "StatusBioDTO":
        """
        Create DTO from database model.

        Args:
            model (Any): database model object

        Returns:
            StatusBioDTO: data transfer object
        """
        data: Dict[str, Any] = {}
        # Iterate over public attributes of the model
        for attr in dir(model):
            if attr.startswith("_"):
                continue
            try:
                value = getattr(model, attr)
            except AttributeError:
                continue
            # Skip methods
            if callable(value):
                continue
            data[attr] = value
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary format.

        Returns:
            dict: dictionary format data
        """
        # Return a shallow copy of the instance's __dict__
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
