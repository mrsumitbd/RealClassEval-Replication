from typing import Any, Dict, List


class FewShotFormat:
    '''Handler for different few-shot example formats'''

    _INPUT_KEYS = (
        'input',
        'prompt',
        'question',
        'instruction',
        'query',
        'src',
        'source',
        'x',
        'context',
        'text',
        'document',
    )
    _OUTPUT_KEYS = (
        'output',
        'completion',
        'answer',
        'response',
        'tgt',
        'target',
        'y',
        'label',
        'summary',
        'target_text',
    )

    @staticmethod
    def _to_str(value: Any) -> str:
        if value is None:
            return ''
        if isinstance(value, bytes):
            try:
                return value.decode('utf-8', errors='replace')
            except Exception:
                return str(value)
        if isinstance(value, (list, tuple)):
            # Flatten lists/tuples of strings
            try:
                return '\n'.join(str(v) for v in value)
            except Exception:
                return str(value)
        if isinstance(value, dict):
            return str(value)
        return str(value)

    @staticmethod
    def _extract_by_keys(obj: Dict[str, Any], keys: tuple) -> Any:
        for k in keys:
            if k in obj:
                return obj[k]
        return None

    @staticmethod
    def _from_messages(obj: Dict[str, Any]) -> Dict[str, str] | None:
        msgs = obj.get('messages')
        if not isinstance(msgs, list):
            return None
        # Normalize messages; expect dicts with role/content
        normalized = []
        for m in msgs:
            if not isinstance(m, dict):
                continue
            role = m.get('role')
            content = m.get('content')
            if role is None and 'speaker' in m:
                role = m.get('speaker')
            if role is None:
                role = 'unknown'
            normalized.append((str(role), FewShotFormat._to_str(content)))

        if not normalized:
            return {'input': '', 'output': ''}

        # Find last assistant message as output
        last_assistant_idx = None
        for i in range(len(normalized) - 1, -1, -1):
            if normalized[i][0].lower() in ('assistant', 'bot', 'model'):
                last_assistant_idx = i
                break

        if last_assistant_idx is not None:
            input_parts = [f'{r}: {c}'.strip()
                           for (r, c) in normalized[:last_assistant_idx]]
            output = normalized[last_assistant_idx][1]
            return {'input': '\n'.join(p for p in input_parts if p), 'output': output}

        # No assistant message; treat whole history as input and empty output
        input_parts = [f'{r}: {c}'.strip() for (r, c) in normalized]
        return {'input': '\n'.join(p for p in input_parts if p), 'output': ''}

    @staticmethod
    def convert(examples: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        '''Convert any supported format to input-output format'''
        if not isinstance(examples, list):
            raise ValueError('examples must be a list of dicts')

        # If already valid, coerce to ensure string typing
        if FewShotFormat.validate(examples):
            coerced: List[Dict[str, str]] = []
            for ex in examples:
                coerced.append(
                    {
                        'input': FewShotFormat._to_str(ex.get('input')),
                        'output': FewShotFormat._to_str(ex.get('output')),
                    }
                )
            return coerced

        converted: List[Dict[str, str]] = []
        for idx, ex in enumerate(examples):
            if not isinstance(ex, dict):
                raise ValueError(f'example at index {idx} is not a dict')

            # Direct mapping if present with other cases
            inp = FewShotFormat._extract_by_keys(ex, FewShotFormat._INPUT_KEYS)
            out = FewShotFormat._extract_by_keys(
                ex, FewShotFormat._OUTPUT_KEYS)

            if inp is not None or out is not None:
                converted.append(
                    {'input': FewShotFormat._to_str(
                        inp), 'output': FewShotFormat._to_str(out)}
                )
                continue

            # Messages-based formats
            msg_pair = FewShotFormat._from_messages(ex)
            if msg_pair is not None:
                converted.append(
                    {'input': FewShotFormat._to_str(
                        msg_pair['input']), 'output': FewShotFormat._to_str(msg_pair['output'])}
                )
                continue

            # If only one textual field exists, assume it is input
            text_keys = [k for k, v in ex.items(
            ) if isinstance(v, (str, bytes))]
            if len(text_keys) == 1:
                converted.append(
                    {'input': FewShotFormat._to_str(ex[text_keys[0]]), 'output': ''})
                continue

            raise ValueError(
                f'could not convert example at index {idx} to input-output format')

        return converted

    @staticmethod
    def validate(examples: List[Dict[str, Any]]) -> bool:
        '''Validate that examples are in input-output format'''
        if not isinstance(examples, list):
            return False
        for ex in examples:
            if not isinstance(ex, dict):
                return False
            if 'input' not in ex or 'output' not in ex:
                return False
            if not isinstance(ex['input'], str) or not isinstance(ex['output'], str):
                return False
        return True
