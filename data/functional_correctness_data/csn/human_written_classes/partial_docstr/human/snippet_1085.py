from typing import TYPE_CHECKING, Any, Callable, Optional

class ConditionDecoder:
    """ Class which provides an object_hook method for decoding dict
  objects into a list when given a condition_decoder. """

    def __init__(self, condition_decoder: Callable[[dict[str, str]], list[Optional[str]]]):
        self.condition_list: list[Optional[str] | list[str]] = []
        self.index = -1
        self.decoder = condition_decoder

    def object_hook(self, object_dict: dict[str, str]) -> int:
        """ Hook which when passed into a json.JSONDecoder will replace each dict
    in a json string with its index and convert the dict to an object as defined
    by the passed in condition_decoder. The newly created condition object is
    appended to the conditions_list.

    Args:
      object_dict: Dict representing an object.

    Returns:
      An index which will be used as the placeholder in the condition_structure
    """
        instance = self.decoder(object_dict)
        self.condition_list.append(instance)
        self.index += 1
        return self.index