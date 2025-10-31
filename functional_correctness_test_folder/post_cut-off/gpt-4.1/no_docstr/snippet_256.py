
from typing import Dict, Any
import re


class PromptPatternMatcher:

    def __init__(self):
        pass

    def analyze_prompt(self, prompt: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        result = {
            "tool_name_found": False,
            "arguments_found": {},
            "missing_arguments": [],
            "extra_arguments": [],
        }

        # Check if tool_name is present in prompt (case-insensitive)
        if re.search(r'\b' + re.escape(tool_name) + r'\b', prompt, re.IGNORECASE):
            result["tool_name_found"] = True

        # Check for each argument if its value is present in the prompt
        for arg, value in arguments.items():
            found = False
            if isinstance(value, str):
                if value and re.search(re.escape(value), prompt, re.IGNORECASE):
                    found = True
            elif isinstance(value, (int, float)):
                if re.search(r'\b' + re.escape(str(value)) + r'\b', prompt):
                    found = True
            elif isinstance(value, list):
                found = all(
                    (isinstance(v, str) and v and re.search(
                        re.escape(v), prompt, re.IGNORECASE))
                    or (isinstance(v, (int, float)) and re.search(r'\b' + re.escape(str(v)) + r'\b', prompt))
                    for v in value
                )
            else:
                # For other types, just do a string search
                if value and re.search(re.escape(str(value)), prompt, re.IGNORECASE):
                    found = True
            result["arguments_found"][arg] = found
            if not found:
                result["missing_arguments"].append(arg)

        # Find extra arguments mentioned in the prompt (simple heuristic: look for words after tool_name)
        extra_args = []
        if result["tool_name_found"]:
            # Find the tool_name in the prompt and extract following words
            pattern = re.compile(
                r'\b' + re.escape(tool_name) + r'\b(.*)', re.IGNORECASE)
            match = pattern.search(prompt)
            if match:
                after_tool = match.group(1)
                # Split into words, remove punctuation
                words = re.findall(r'\b\w+\b', after_tool)
                # Remove argument values that are already in arguments
                arg_values = set()
                for v in arguments.values():
                    if isinstance(v, list):
                        arg_values.update(str(x).lower() for x in v)
                    else:
                        arg_values.add(str(v).lower())
                for w in words:
                    if w.lower() not in arg_values and w.lower() not in arguments.keys():
                        extra_args.append(w)
        result["extra_arguments"] = extra_args

        return result
