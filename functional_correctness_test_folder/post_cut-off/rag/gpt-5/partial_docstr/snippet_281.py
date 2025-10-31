from typing import List, Dict, Any


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
            if isinstance(value, (str, int, float, bool)):
                return str(value)
            return str(value)

        def handle_messages(msgs: Any) -> Dict[str, str]:
            if not isinstance(msgs, list):
                raise ValueError('messages must be a list')
            # Find the rightmost adjacent (user, assistant) pair
            for i in range(len(msgs) - 1, 0, -1):
                m_prev = msgs[i - 1]
                m_curr = msgs[i]
                if (
                    isinstance(m_prev, dict)
                    and isinstance(m_curr, dict)
                    and m_prev.get('role') == 'user'
                    and m_curr.get('role') == 'assistant'
                ):
                    return {
                        'input': to_str(m_prev.get('content')),
                        'output': to_str(m_curr.get('content')),
                    }
            # Fallback: find last user with any assistant after it
            last_user_idx = None
            for i, m in enumerate(msgs):
                if isinstance(m, dict) and m.get('role') == 'user':
                    last_user_idx = i
            if last_user_idx is not None:
                for j in range(last_user_idx + 1, len(msgs)):
                    m = msgs[j]
                    if isinstance(m, dict) and m.get('role') == 'assistant':
                        return {
                            'input': to_str(msgs[last_user_idx].get('content')),
                            'output': to_str(m.get('content')),
                        }
            raise ValueError('could not derive input/output from messages')

        converted: List[Dict[str, str]] = []

        for ex in examples:
            if not isinstance(ex, dict):
                raise TypeError('each example must be a dict')

            # Already in desired format
            if 'input' in ex and 'output' in ex:
                converted.append(
                    {'input': to_str(ex['input']), 'output': to_str(ex['output'])})
                continue

            # Alpaca-style: instruction + optional input -> output
            if 'instruction' in ex and ('output' in ex or 'response' in ex):
                instr = to_str(ex.get('instruction'))
                inp = ex.get('input')
                inp_s = to_str(inp) if inp not in (None, '') else ''
                input_text = f'Instruction: {instr}'
                if inp_s:
                    input_text = f'{input_text}\n\nInput: {inp_s}'
                output_text = to_str(ex.get('output', ex.get('response')))
                converted.append({'input': input_text, 'output': output_text})
                continue

            # Prompt/completion
            if 'prompt' in ex and ('completion' in ex or 'output' in ex or 'response' in ex):
                converted.append(
                    {'input': to_str(ex.get('prompt')), 'output': to_str(
                        ex.get('completion', ex.get('output', ex.get('response'))))}
                )
                continue

            # Question/Answer (+ optional context/passage/source)
            if ('question' in ex or 'query' in ex) and (
                'answer' in ex or 'response' in ex or 'output' in ex or 'completion' in ex
            ):
                question = to_str(ex.get('question', ex.get('query')))
                context = ex.get('context', ex.get(
                    'passage', ex.get('source')))
                if context not in (None, ''):
                    input_text = f'{to_str(context)}\n\nQuestion: {question}'
                else:
                    input_text = question
                output_text = to_str(ex.get('answer', ex.get(
                    'response', ex.get('output', ex.get('completion')))))
                converted.append({'input': input_text, 'output': output_text})
                continue

            # Text classification style: text -> label/target
            if 'text' in ex and any(k in ex for k in ('label', 'target', 'output', 'response', 'completion')):
                output_val = ex.get('label', ex.get('target', ex.get(
                    'output', ex.get('response', ex.get('completion')))))
                converted.append(
                    {'input': to_str(ex.get('text')), 'output': to_str(output_val)})
                continue

            # Generic pair X/y or src/tgt
            if 'X' in ex and 'y' in ex:
                converted.append(
                    {'input': to_str(ex.get('X')), 'output': to_str(ex.get('y'))})
                continue
            if 'src' in ex and 'tgt' in ex:
                converted.append(
                    {'input': to_str(ex.get('src')), 'output': to_str(ex.get('tgt'))})
                continue

            # Summarization: document -> summary
            if ('document' in ex or 'article' in ex or 'text' in ex) and ('summary' in ex or 'abstract' in ex):
                inp = ex.get('document', ex.get('article', ex.get('text')))
                out = ex.get('summary', ex.get('abstract'))
                converted.append({'input': to_str(inp), 'output': to_str(out)})
                continue

            # messages chat format
            if 'messages' in ex:
                converted.append(handle_messages(ex.get('messages')))
                continue

            # input_text/output_text
            if 'input_text' in ex and 'output_text' in ex:
                converted.append({'input': to_str(
                    ex.get('input_text')), 'output': to_str(ex.get('output_text'))})
                continue

            # Fallback: try single input-like and output-like keys
            input_keys = ('input', 'instruction', 'prompt', 'question',
                          'query', 'text', 'document', 'article', 'src')
            output_keys = ('output', 'response', 'completion', 'answer',
                           'label', 'target', 'summary', 'tgt', 'abstract')
            found_inp = next((k for k in input_keys if k in ex), None)
            found_out = next((k for k in output_keys if k in ex), None)
            if found_inp and found_out:
                converted.append(
                    {'input': to_str(ex.get(found_inp)), 'output': to_str(ex.get(found_out))})
                continue

            raise ValueError(
                f'Unsupported example format: keys={list(ex.keys())}')

        return converted

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
