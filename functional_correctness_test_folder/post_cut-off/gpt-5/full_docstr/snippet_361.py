from typing import Any, Optional, Dict
import re
import json
from uuid import uuid4

try:
    from pydantic import BaseModel as PydanticBaseModelV2  # type: ignore
except Exception:
    PydanticBaseModelV2 = None  # type: ignore

try:
    from pydantic.v1 import BaseModel as PydanticBaseModelV1  # type: ignore
except Exception:
    PydanticBaseModelV1 = None  # type: ignore

try:
    from langchain_core.messages import ToolCall
except Exception:
    # Minimal fallback dataclass if langchain_core is not available
    from dataclasses import dataclass

    @dataclass
    class ToolCall:
        id: str
        name: str
        args: Any


class OCIUtils:
    '''Utility functions for OCI Generative AI integration.'''

    @staticmethod
    def is_pydantic_class(obj: Any) -> bool:
        '''Check if an object is a Pydantic BaseModel subclass.'''
        # If it's an instance, check its class
        cls = obj if isinstance(obj, type) else obj.__class__

        def _is_subclass(candidate, base) -> bool:
            try:
                return isinstance(candidate, type) and isinstance(base, type) and issubclass(candidate, base)
            except Exception:
                return False
        return any(
            _is_subclass(cls, base)
            for base in (PydanticBaseModelV2, PydanticBaseModelV1)
            if base is not None
        )

    @staticmethod
    def remove_signature_from_tool_description(name: str, description: str) -> str:
        '''
        Remove the tool signature and Args section from a tool description.
        The signature is typically prefixed to the description and followed
        by an Args section.
        '''
        if not description:
            return ""
        text = description.strip()

        # Remove leading function signature like "name(arg1: str, ...):"
        # Also handle optional return annotation and trailing colon.
        sig_pattern = r'^\s*`?\s*' + \
            re.escape(name) + r'\s*\([^)]*\)\s*(?:->\s*[^\s:]+)?\s*:?\s*`?\s*'
        text = re.sub(sig_pattern, '', text, count=1,
                      flags=re.IGNORECASE | re.MULTILINE)

        # Remove Args/Arguments/Parameters sections up to the next top-level header-like token or end
        # Matches e.g. "Args:\n  x: ...\n  y: ...\nReturns: ..."
        section_names = ['Args', 'Arguments', 'Parameters']
        for section in section_names:
            pattern = rf'(?is)\b{section}:\s*.*?(?=\n[A-Z][A-Za-z ]{{1,30}}:\s*|\Z)'
            text = re.sub(pattern, '', text)

        # Collapse extra blank lines and trim
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()

    @staticmethod
    def convert_oci_tool_call_to_langchain(tool_call: Any) -> ToolCall:
        '''Convert an OCI tool call to a LangChain ToolCall.'''
        def get_attr(obj: Any, *keys: str) -> Optional[Any]:
            if obj is None:
                return None
            # dict lookup
            if isinstance(obj, dict):
                for k in keys:
                    if k in obj:
                        return obj[k]
            # attribute lookup
            for k in keys:
                if hasattr(obj, k):
                    return getattr(obj, k)
            return None

        # Extract fields with fallbacks
        name = get_attr(tool_call, 'name', 'function',
                        'function_name', 'tool_name')
        args = get_attr(tool_call, 'arguments', 'args',
                        'parameters', 'input', 'payload')
        call_id = get_attr(tool_call, 'id', 'call_id', 'tool_call_id')

        if name is None:
            # Some OCI payloads may wrap the function under "function" dict with "name" and "arguments"
            func = get_attr(tool_call, 'function')
            name = get_attr(func, 'name') if func is not None else None
            if args is None and func is not None:
                args = get_attr(func, 'arguments')

        # Normalize args to dict when possible
        parsed_args: Any = args
        if isinstance(args, (bytes, bytearray)):
            try:
                parsed_args = json.loads(args.decode('utf-8'))
            except Exception:
                parsed_args = args.decode('utf-8', errors='ignore')
        elif isinstance(args, str):
            s = args.strip()
            try:
                parsed_args = json.loads(s)
            except Exception:
                # Try to coerce simple key=value comma pairs if present
                if '=' in s and ',' in s:
                    kv: Dict[str, Any] = {}
                    for part in s.split(','):
                        if '=' in part:
                            k, v = part.split('=', 1)
                            kv[k.strip()] = v.strip()
                    parsed_args = kv if kv else s
                else:
                    parsed_args = s
        elif args is None:
            parsed_args = {}

        if call_id is None:
            call_id = f"toolcall-{uuid4().hex}"

        if not name:
            name = "unknown_tool"

        return ToolCall(id=str(call_id), name=str(name), args=parsed_args)
