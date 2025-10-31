
from enum import Enum
from typing import Any, Dict, List, Optional, Type


class Element:
    """
    A flexible container that can be populated from dictionaries and can
    create nested structures of Elements or lists of Elements.
    """

    def set_common_datas(self, element: "Element", name: str, datas: Dict[str, Any]) -> None:
        """
        Set an attribute on *element* if *name* exists in *datas*.
        """
        if name in datas:
            setattr(element, name, datas[name])

    def create_dictionary_of_element_from_dictionary(
        self, property_name: str, datas: Dict[str, Any]
    ) -> Dict[str, "Element"]:
        """
        Create a dictionary of Element instances from a nested dictionary
        located at *property_name* inside *datas*.
        """
        result: Dict[str, Element] = {}
        sub_dict = datas.get(property_name, {})
        if not isinstance(sub_dict, dict):
            return result

        for key, value in sub_dict.items():
            el = Element()
            if isinstance(value, dict):
                for k, v in value.items():
                    setattr(el, k, v)
            else:
                # If the value is not a dict, store it under a generic key
                setattr(el, "value", value)
            result[key] = el
        return result

    def create_list_of_element_from_dictionary(
        self, property_name: str, datas: Dict[str, Any]
    ) -> List["Element"]:
        """
        Create a list of Element instances from a list located at
        *property_name* inside *datas*.
        """
        result: List[Element] = []
        sub_list = datas.get(property_name, [])
        if not isinstance(sub_list, list):
            return result

        for item in sub_list:
            el = Element()
            if isinstance(item, dict):
                for k, v in item.items():
                    setattr(el, k, v)
            else:
                setattr(el, "value", item)
            result.append(el)
        return result

    def get_enum(
        self, property: str, enum: Type[Enum], datas: Dict[str, Any]
    ) -> Optional[Enum]:
        """
        Retrieve an Enum member from *datas* using *property* as the key.
        Supports both integer/enum value lookup and name lookup.
        """
        if property not in datas:
            return None

        val = datas[property]
        try:
            # Try to construct the enum from the value directly
            return enum(val)
        except Exception:
            # Fallback to name lookup if the value is a string
            try:
                return enum[val]
            except Exception:
                return None
