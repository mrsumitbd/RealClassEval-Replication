
from typing import Any, Dict, List, Optional, Type, TypeVar
from enum import Enum

T = TypeVar('T')


class Element:
    """
    Utility class providing helper methods for populating objects from dictionaries.
    """

    def set_common_datas(self, element: Any, name: str, datas: Dict[str, Any]) -> None:
        """
        Set attributes on *element* based on the keys present in *datas*.
        If *name* is a key in *datas*, the corresponding value is assigned to
        the attribute of the same name on *element*.
        Additionally, any key in *datas* that matches an existing attribute
        on *element* will be set.

        Parameters
        ----------
        element : Any
            The object whose attributes will be set.
        name : str
            The primary key to look for in *datas*.
        datas : Dict[str, Any]
            Dictionary containing data to populate *element*.
        """
        # Set the primary attribute if present
        if name in datas:
            setattr(element, name, datas[name])

        # Set any other matching attributes
        for key, value in datas.items():
            if hasattr(element, key):
                setattr(element, key, value)

    def create_dictionary_of_element_from_dictionary(
        self,
        property_name: str,
        datas: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Retrieve a dictionary from *datas* under *property_name*.
        If the property is missing or not a dictionary, an empty dictionary
        is returned.

        Parameters
        ----------
        property_name : str
            Key in *datas* that should contain a dictionary.
        datas : Dict[str, Any]
            Source dictionary.

        Returns
        -------
        Dict[str, Any]
            The dictionary found under *property_name*, or an empty dict.
        """
        value = datas.get(property_name)
        if isinstance(value, dict):
            return value
        return {}

    def create_list_of_element_from_dictionary(
        self,
        property_name: str,
        datas: Dict[str, Any]
    ) -> List[Any]:
        """
        Retrieve a list from *datas* under *property_name*.
        If the property is missing or not a list, an empty list is returned.

        Parameters
        ----------
        property_name : str
            Key in *datas* that should contain a list.
        datas : Dict[str, Any]
            Source dictionary.

        Returns
        -------
        List[Any]
            The list found under *property_name*, or an empty list.
        """
        value = datas.get(property_name)
        if isinstance(value, list):
            return value
        return []

    def get_enum(
        self,
        property: str,
        enum: Type[Enum],
        datas: Dict[str, Any]
    ) -> Optional[Enum]:
        """
        Convert a value from *datas* into an enum member.

        Parameters
        ----------
        property : str
            Key in *datas* whose value should be converted.
        enum : Type[Enum]
            The Enum class to instantiate.
        datas : Dict[str, Any]
            Source dictionary.

        Returns
        -------
        Optional[Enum]
            The enum member corresponding to the value, or None if the key
            is missing or the value is not a valid enum member.
        """
        if property not in datas:
            return None

        value = datas[property]
        try:
            return enum(value)
        except (ValueError, TypeError):
            return None
