from typing import List, Dict, Iterable, Optional

class GrFNState:

    def __init__(self, lambda_strings: Optional[List[str]], last_definitions: Optional[Dict]={}, next_definitions: Optional[Dict]={}, last_definition_default=0, function_name=None, variable_types: Optional[Dict]={}, start: Optional[Dict]={}, scope_path: Optional[List]=[], arrays: Optional[Dict]={}, array_types: Optional[Dict]={}, array_assign_name: Optional=None, string_assign_name: Optional=None):
        self.lambda_strings = lambda_strings
        self.last_definitions = last_definitions
        self.next_definitions = next_definitions
        self.last_definition_default = last_definition_default
        self.function_name = function_name
        self.variable_types = variable_types
        self.start = start
        self.scope_path = scope_path
        self.arrays = arrays
        self.array_types = array_types
        self.array_assign_name = array_assign_name
        self.string_assign_name = string_assign_name

    def copy(self, lambda_strings: Optional[List[str]]=None, last_definitions: Optional[Dict]=None, next_definitions: Optional[Dict]=None, last_definition_default=None, function_name=None, variable_types: Optional[Dict]=None, start: Optional[Dict]=None, scope_path: Optional[List]=None, arrays: Optional[Dict]=None, array_types: Optional[Dict]=None, array_assign_name: Optional=None, string_assign_name: Optional=None):
        return GrFNState(self.lambda_strings if lambda_strings is None else lambda_strings, self.last_definitions if last_definitions is None else last_definitions, self.next_definitions if next_definitions is None else next_definitions, self.last_definition_default if last_definition_default is None else last_definition_default, self.function_name if function_name is None else function_name, self.variable_types if variable_types is None else variable_types, self.start if start is None else start, self.scope_path if scope_path is None else scope_path, self.arrays if arrays is None else arrays, self.array_types if array_types is None else array_types, self.array_assign_name if array_assign_name is None else array_assign_name, self.string_assign_name if string_assign_name is None else string_assign_name)