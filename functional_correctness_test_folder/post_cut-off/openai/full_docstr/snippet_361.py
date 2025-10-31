
from __future__ import annotations

import json
import re
from typing import Any

from langchain.schema import ToolCall
from pydantic import BaseModel


class OCIUtils:
    '''Utility functions for OCI Generative AI integration.'''

    @staticmethod
    def is_pydantic_class(obj: Any) -> bool:
        '''Check if an object is a Pydantic BaseModel subclass.'''
        return isinstance(obj, type) and issubclass(obj, BaseModel)

    @staticmethod
    def remove_signature_from_tool_description(name: str, description: str) -> str:
        '''
        Remove the tool signature and Args section from a tool description.
        The signature is typically prefixed to the description and followed
        by an Args section.
        '''
        # Split into lines
        lines = description.splitlines()
        cleaned_lines = []

        # Flag to skip signature line
        skip_signature = False
        # Flag to skip Args section
        skip_args_section = False

        for line in lines:
            stripped = line.strip()

            # Detect signature line (e.g., "def tool_name(arg1: type, arg2: type) -> return_type:")
            if not skip_signature and re.match(r'^\w+\s*\(.*\)\s*(:|->)', stripped):
                skip_signature = True
                continue

            # Detect start of Args section
            if not skip_args_section and stripped.lower().startswith('args:'):
                skip_args_section = True
                continue

            if skip_args_section:
                # Skip lines until an empty line or a line that does not start with whitespace
                if stripped == '' or not line.startswith(' '):
                    skip_args_section = False
                else:
                    continue

            if not skip_signature:
                cleaned_lines.append(line)

        return '\n'.join(cleaned_lines).strip()

    @staticmethod
    def convert_oci_tool_call_to_langchain(tool_call: Any) -> ToolCall:
        '''Convert an OCI tool call to a LangChain ToolCall.'''
        # Extract name
        name = getattr(tool_call, 'name', None)
        if name is None:
            raise ValueError('OCI tool call must have a "name" attribute')

        # Extract arguments
        args = getattr(tool_call, 'arguments', {})
        if isinstance(args, dict):
            arguments_json = json.dumps(args, ensure_ascii=False)
        elif isinstance(args, str):
            arguments_json = args
        else:
            raise TypeError('OCI tool call "arguments" must be dict or str')

        # Extract id if present
        call_id = getattr(tool_call, 'id', '')

        return ToolCall(id=call_id, name=name, arguments=arguments_json)
