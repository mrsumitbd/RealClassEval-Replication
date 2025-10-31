from typing import List, Dict, Any, Optional


class FewShotFormat:
    '''Handler for different few-shot example formats'''

    _INPUT_KEYS = ("input", "prompt", "instruction",
                   "question", "text", "source")
    _OUTPUT_KEYS = ("output", "completion", "answer", "target", "response")

    _CONTEXT_KEYS = ("context", "passage", "document")
    _QUESTION_KEYS = ("question", "query")

    @staticmethod
    def convert(examples: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        '''Convert any supported format to input-output format'''
        if not isinstance(examples, list):
            raise TypeError("examples must be a list of dicts")

        converted: List[Dict[str, str]] = []
        for i, ex in enumerate(examples):
            if not isinstance(ex, dict):
                raise TypeError(f"example at index {i} is not a dict")

            # Case 1: Already input-output
            in_val = FewShotFormat._find_first_key(
                ex, FewShotFormat._INPUT_KEYS)
            out_val = FewShotFormat._find_first_key(
                ex, FewShotFormat._OUTPUT_KEYS)
            if in_val is not None and out_val is not None:
                converted.append({"input": FewShotFormat._to_str(
                    in_val), "output": FewShotFormat._to_str(out_val)})
                continue

            # Case 2: context + question + answer
            ctx_val = FewShotFormat._find_first_key(
                ex, FewShotFormat._CONTEXT_KEYS)
            q_val = FewShotFormat._find_first_key(
                ex, FewShotFormat._QUESTION_KEYS)
            a_val = FewShotFormat._find_first_key(
                ex, FewShotFormat._OUTPUT_KEYS)
            if q_val is not None and a_val is not None:
                parts = []
                if ctx_val is not None:
                    parts.append(FewShotFormat._label_and_str(
                        "Context", ctx_val))
                parts.append(FewShotFormat._label_and_str("Question", q_val))
                input_str = "\n\n".join(parts)
                converted.append(
                    {"input": input_str, "output": FewShotFormat._to_str(a_val)})
                continue

            # Case 3: chat messages
            if "messages" in ex and isinstance(ex["messages"], list):
                msg_list = ex["messages"]
                if not msg_list:
                    raise ValueError(
                        f"example at index {i} has empty messages")

                # normalize messages to dicts with role/content
                norm_msgs = []
                for j, m in enumerate(msg_list):
                    if isinstance(m, dict):
                        role = m.get("role")
                        content = m.get("content")
                    elif isinstance(m, (list, tuple)) and len(m) == 2:
                        role, content = m[0], m[1]
                    else:
                        raise ValueError(
                            f"example at index {i} has invalid message at position {j}")
                    if not isinstance(role, str) or not isinstance(content, str):
                        role = str(role) if role is not None else ""
                        content = "" if content is None else str(content)
                    norm_msgs.append({"role": role, "content": content})

                # Find last assistant message as output
                last_assistant_idx = None
                for idx in range(len(norm_msgs) - 1, -1, -1):
                    if norm_msgs[idx]["role"].lower() in ("assistant", "bot", "system_reply"):
                        last_assistant_idx = idx
                        break

                if last_assistant_idx is None:
                    raise ValueError(
                        f"example at index {i} has no assistant message for output")

                output_str = norm_msgs[last_assistant_idx]["content"]

                # Input is all messages before last assistant
                pre_msgs = norm_msgs[:last_assistant_idx]
                if not pre_msgs:
                    raise ValueError(
                        f"example at index {i} has no preceding messages to form input")

                input_lines = []
                for m in pre_msgs:
                    role = m["role"].lower()
                    role_name = "assistant" if role in (
                        "assistant", "bot") else "user" if role in ("user", "client") else role
                    input_lines.append(f"{role_name}: {m['content']}")
                input_str = "\n".join(input_lines)

                converted.append({"input": input_str, "output": output_str})
                continue

            raise ValueError(
                f"example at index {i} could not be converted; provide input/output or supported fields")

        return converted

    @staticmethod
    def validate(examples: List[Dict[str, Any]]) -> bool:
        '''Validate that examples are in input-output format'''
        if not isinstance(examples, list):
            return False
        for ex in examples:
            if not isinstance(ex, dict):
                return False
            if "input" not in ex or "output" not in ex:
                return False
            if not isinstance(ex["input"], str) or not isinstance(ex["output"], str):
                return False
        return True

    @staticmethod
    def _find_first_key(d: Dict[str, Any], keys: tuple) -> Optional[Any]:
        for k in keys:
            if k in d:
                return d[k]
        return None

    @staticmethod
    def _to_str(value: Any) -> str:
        return "" if value is None else (value if isinstance(value, str) else str(value))

    @staticmethod
    def _label_and_str(label: str, value: Any) -> str:
        return f"{label}: {FewShotFormat._to_str(value)}"
