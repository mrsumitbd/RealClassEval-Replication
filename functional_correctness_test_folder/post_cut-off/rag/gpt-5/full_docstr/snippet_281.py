from typing import List, Dict, Any
import json


class FewShotFormat:
    """Handler for different few-shot example formats"""

    @staticmethod
    def convert(examples: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Convert any supported format to input-output format"""
        if not isinstance(examples, list):
            raise TypeError('examples must be a list of dicts')

        def to_str(value: Any) -> str:
            if value is None:
                return ''
            if isinstance(value, str):
                return value.strip()
            if isinstance(value, (dict, list)):
                return json.dumps(value, ensure_ascii=False)
            return str(value).strip()

        candidate_pairs = [
            ('input', 'output'),
            ('prompt', 'completion'),
            ('question', 'answer'),
            ('instruction', 'response'),
            ('instruction', 'output'),
            ('context', 'response'),
            ('query', 'response'),
            ('source', 'target'),
            ('input_text', 'target_text'),
            ('text', 'label'),
        ]

        results: List[Dict[str, str]] = []

        for ex in examples:
            if not isinstance(ex, dict):
                raise TypeError('each example must be a dict')

            matched = False

            # Direct key-pair mapping
            for ki, ko in candidate_pairs:
                if ki in ex and ko in ex:
                    results.append(
                        {'input': to_str(ex[ki]), 'output': to_str(ex[ko])})
                    matched = True
                    break
            if matched:
                continue

            # Chat messages format
            if 'messages' in ex and isinstance(ex['messages'], list):
                messages = ex['messages']
                last_assistant_idx = None
                for idx in range(len(messages) - 1, -1, -1):
                    m = messages[idx] if isinstance(
                        messages[idx], dict) else {}
                    role = str(m.get('role', '')).lower()
                    if role == 'assistant':
                        last_assistant_idx = idx
                        break
                if last_assistant_idx is None:
                    raise ValueError(
                        'messages format requires at least one assistant message as output')

                output_text = to_str(
                    (messages[last_assistant_idx] or {}).get('content', ''))

                parts = []
                for m in messages[:last_assistant_idx]:
                    if not isinstance(m, dict):
                        continue
                    role = to_str(m.get('role', ''))
                    content = to_str(m.get('content', ''))
                    if role and content:
                        parts.append(f'{role}: {content}')
                    elif content:
                        parts.append(content)
                input_text = '\n'.join(parts).strip()
                results.append({'input': input_text, 'output': output_text})
                continue

            # Heuristic fallback: try to find any input-like and output-like keys
            input_like_key_candidates = [
                'input', 'prompt', 'question', 'instruction', 'context', 'query', 'source', 'input_text', 'text'
            ]
            output_like_key_candidates = [
                'output', 'completion', 'answer', 'response', 'target', 'target_text', 'label'
            ]

            input_like = None
            output_like = None

            for k in input_like_key_candidates:
                if k in ex:
                    input_like = ex[k]
                    break
            for k in output_like_key_candidates:
                if k in ex:
                    output_like = ex[k]
                    break

            if input_like is not None and output_like is not None:
                results.append({'input': to_str(input_like),
                               'output': to_str(output_like)})
                continue

            raise ValueError(
                f'Unsupported example format: keys={list(ex.keys())}')

        if not FewShotFormat.validate(results):
            raise ValueError(
                'conversion resulted in invalid input-output format')

        return results

    @staticmethod
    def validate(examples: List[Dict[str, Any]]) -> bool:
        """Validate that examples are in input-output format"""
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
