from typing import Any, Dict, List, Set, Tuple
import re


class PromptPatternMatcher:
    def __init__(self):
        self._placeholder_re = re.compile(
            r"(?<!\{)\{([a-zA-Z_][a-zA-Z0-9_]*)\}(?!\})")
        self._kv_re = re.compile(
            r"""(?P<key>[A-Za-z_][A-Za-z0-9_\.]*)\s*(=|:)\s*(?P<value>("([^"\\]|\\.)*"|'([^'\\]|\\.)*'|`([^`\\]|\\.)*`|[^\s,;]+))""",
            re.VERBOSE,
        )

    def _strip_quotes(self, s: str) -> str:
        if len(s) >= 2 and s[0] == s[-1] and s[0] in {'"', "'", "`"}:
            return s[1:-1]
        return s

    def _find_placeholders(self, prompt: str) -> List[str]:
        return list(dict.fromkeys(self._placeholder_re.findall(prompt)))

    def _extract_kv_pairs(self, prompt: str) -> Dict[str, Any]:
        extracted: Dict[str, Any] = {}
        for m in self._kv_re.finditer(prompt):
            key = m.group("key")
            val_raw = m.group("value")
            val = self._strip_quotes(val_raw)

            if val.lower() in {"true", "false"}:
                coerced: Any = val.lower() == "true"
            else:
                try:
                    if re.fullmatch(r"[-+]?\d+", val):
                        coerced = int(val)
                    elif re.fullmatch(r"[-+]?(?:\d*\.\d+|\d+\.\d*)(?:[eE][-+]?\d+)?", val):
                        coerced = float(val)
                    else:
                        coerced = val
                except Exception:
                    coerced = val

            extracted[key] = coerced
        return extracted

    def _detect_tool_name(self, prompt: str, tool_name: str) -> Tuple[bool, str]:
        if not tool_name:
            return False, ""
        pattern = re.compile(rf"\b{re.escape(tool_name)}\b", re.IGNORECASE)
        m = pattern.search(prompt)
        return (m is not None, m.group(0) if m else "")

    def _type_name(self, v: Any) -> str:
        return type(v).__name__

    def analyze_prompt(self, prompt: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        prompt = prompt or ""
        tool_name = tool_name or ""
        arguments = arguments or {}

        placeholders = self._find_placeholders(prompt)
        kv_extracted = self._extract_kv_pairs(prompt)

        provided_keys: Set[str] = set(arguments.keys())
        placeholder_set: Set[str] = set(placeholders)

        missing_arguments = sorted(list(placeholder_set - provided_keys))
        extra_arguments = sorted(list(provided_keys - placeholder_set))

        tool_match, detected_tool_token = self._detect_tool_name(
            prompt, tool_name)

        overlaps = sorted(list(placeholder_set & set(kv_extracted.keys())))
        extracted_arguments = {k: kv_extracted[k] for k in overlaps}

        score = 0.0
        if tool_match:
            score += 0.5
        if not missing_arguments and placeholder_set:
            score += 0.3
        if not extra_arguments and provided_keys:
            score += 0.1
        if extracted_arguments:
            score += 0.1
        score = max(0.0, min(1.0, score))

        result = {
            "tool_name_match": tool_match,
            "detected_tool_token": detected_tool_token,
            "placeholders": placeholders,
            "provided_arguments": dict(arguments),
            "missing_arguments": missing_arguments,
            "extra_arguments": extra_arguments,
            "extracted_arguments_from_prompt": extracted_arguments,
            "all_extracted_kv_pairs": kv_extracted,
            "argument_types": {k: self._type_name(v) for k, v in arguments.items()},
            "score": score,
            "matches": score >= 0.6,
        }
        return result
