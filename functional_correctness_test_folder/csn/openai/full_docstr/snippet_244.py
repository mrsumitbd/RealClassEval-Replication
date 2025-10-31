
from types import SimpleNamespace
from enum import Enum
from typing import Any, Dict, List, Optional, Type


class Element:
    ''' Populate Helper Factory
    '''

    def set_common_datas(self, element: SimpleNamespace, name: Optional[str], datas: Dict[str, Any]) -> SimpleNamespace:
        '''Populated common data for an element from dictionnary datas
        '''
        if name is not None:
            setattr(element, 'name', name)
        for key, value in datas.items():
            setattr(element, key, value)
        return element

    def create_dictionary_of_element_from_dictionary(self, property_name: str, datas: Dict[str, Any]) -> Dict[str, SimpleNamespace]:
        '''Populate a dictionary of elements
        '''
        result: Dict[str, SimpleNamespace] = {}
        sub_dict = datas.get(property_name)
        if isinstance(sub_dict, dict):
            for key, sub_datas in sub_dict.items():
                if isinstance(sub_datas, dict):
                    elem = SimpleNamespace()
                    self.set_common_datas(elem, key, sub_datas)
                    result[key] = elem
        return result

    def create_list_of_element_from_dictionary(self, property_name: str, datas: Dict[str, Any]) -> List[SimpleNamespace]:
        '''Populate a list of elements
        '''
        result: List[SimpleNamespace] = []
        sub_list = datas.get(property_name)
        if isinstance(sub_list, list):
            for sub_datas in sub_list:
                if isinstance(sub_datas, dict):
                    elem = SimpleNamespace()
                    self.set_common_datas(elem, None, sub_datas)
                    result.append(elem)
        return result

    def get_enum(self, property: str, enum: Type[Enum], datas: Dict[str, Any]) -> Optional[Enum]:
        '''Factory enum type
        '''
        if property not in datas:
            return None
        value = datas[property]
        try:
            return enum(value)
        except Exception:
            return None
