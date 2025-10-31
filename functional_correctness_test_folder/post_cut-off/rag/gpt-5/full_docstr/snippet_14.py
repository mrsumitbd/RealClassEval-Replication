import random
from typing import Any, Dict, List, Optional, Tuple, Union


class _SafeDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"


def _fmt(template: str, mapping: Dict[str, Any]) -> str:
    return template.format_map(_SafeDict(mapping))


class templater:
    '''Class for generating templates for question and answer generation.
    This class handles the creation of templates for generating both questions
    and answers based on predefined rules and configurations.
    '''

    def __init__(self, q_dict: dict, a_dict: dict, user_name: str = '', global_bio: str = '', is_cot: bool = True):
        '''Initialize the templater with question and answer dictionaries.
        Args:
            q_dict: Dictionary containing question type configurations.
            a_dict: Dictionary containing answer type configurations.
            user_name: Name of the user for personalization.
            global_bio: Global biography for context.
        '''
        self.q_dict: Dict[str, Any] = q_dict or {}
        self.a_dict: Dict[str, Any] = a_dict or {}
        self.user_name: str = user_name or ''
        self.global_bio: str = global_bio or ''
        self.is_cot: bool = bool(is_cot)
        self._rng = random.Random()

    def _resolve_template(self, source: Dict[str, Any], *, key: Optional[str] = None) -> Tuple[str, Dict[str, Any]]:
        cfg: Dict[str, Any] = {}
        if key is not None:
            cfg = source.get(key) or source.get('default') or {}
        else:
            cfg = source

        template = ''
        # Accept one of the following shapes:
        # - {'template': '...'}
        # - {'templates': ['...', '...']}  -> choose first
        # - directly a string
        # - or nested under {'config': {...}}
        if isinstance(cfg, str):
            template = cfg
        elif isinstance(cfg, dict):
            if 'template' in cfg and isinstance(cfg['template'], str):
                template = cfg['template']
            elif 'templates' in cfg and isinstance(cfg['templates'], list) and cfg['templates']:
                template = cfg['templates'][0]
            elif 'config' in cfg and isinstance(cfg['config'], dict):
                c2 = cfg['config']
                if isinstance(c2.get('template'), str):
                    template = c2['template']
                elif isinstance(c2.get('templates'), list) and c2['templates']:
                    template = c2['templates'][0]
        if not template:
            template = ''
        return template, cfg if isinstance(cfg, dict) else {}

    def _apply_wrappers(self, text: str, cfg: Dict[str, Any]) -> str:
        prefix = cfg.get('prefix', '')
        suffix = cfg.get('suffix', '')
        return f'{prefix}{text}{suffix}'

    def _fill_common(self, text: str, extra: Optional[Dict[str, Any]] = None) -> str:
        mapping = {
            'user_name': self.user_name,
            'global_bio': self.global_bio,
        }
        if extra:
            mapping.update(extra)
        return _fmt(text, mapping)

    def _choose_optionals(self, optional_cfg: Any) -> Tuple[List[str], List[str]]:
        chosen_names: List[str] = []
        chosen_texts: List[str] = []
        if not optional_cfg:
            return chosen_names, chosen_texts

        # Normalize to list of option items: {'name': str, 'text': str, 'p': float, 'required': bool, 'weight': float}
        items: List[Dict[str, Any]] = []

        # Support shapes:
        # - {'types': {'foo': 'text', 'bar': {'text': '...', 'p': 0.7}}, 'k': 1}
        # - {'foo': 'text', 'bar': {'text': '...', 'p': 0.7}}
        # - [{'name': 'foo', 'text': '...'}, ...]
        # - list of strings
        container = optional_cfg.get('types', optional_cfg) if isinstance(
            optional_cfg, dict) else optional_cfg

        if isinstance(container, dict):
            for name, val in container.items():
                if isinstance(val, str):
                    items.append({'name': name, 'text': val})
                elif isinstance(val, dict):
                    item = {'name': name, 'text': val.get('text', ''), 'p': val.get(
                        'p'), 'required': val.get('required', False), 'weight': val.get('weight')}
                    items.append(item)
        elif isinstance(container, list):
            for idx, val in enumerate(container):
                if isinstance(val, str):
                    items.append({'name': f'opt_{idx}', 'text': val})
                elif isinstance(val, dict):
                    name = val.get('name', f'opt_{idx}')
                    item = {'name': name, 'text': val.get('text', ''), 'p': val.get(
                        'p'), 'required': val.get('required', False), 'weight': val.get('weight')}
                    items.append(item)

        if not items:
            return chosen_names, chosen_texts

        # Required go first
        for it in items:
            if it.get('required'):
                chosen_names.append(it['name'])
                chosen_texts.append(it.get('text', ''))

        # Remaining
        remaining = [it for it in items if not it.get('required')]
        k = optional_cfg.get('k')
        strategy = optional_cfg.get('strategy')
        default_p = optional_cfg.get('prob', 0.5)

        if isinstance(k, int) and k > 0:
            weights = [float(it.get('weight', 1.0)) for it in remaining]
            # Simple weighted sample without replacement
            pool = remaining[:]
            picks = min(k, len(pool))
            for _ in range(picks):
                total = sum(weights)
                if total <= 0:
                    choice = self._rng.choice(pool)
                    idx = pool.index(choice)
                else:
                    r = self._rng.random() * total
                    acc = 0.0
                    idx = 0
                    for i, w in enumerate(weights):
                        acc += w
                        if r <= acc:
                            idx = i
                            break
                choice = pool.pop(idx)
                weights.pop(idx)
                chosen_names.append(choice['name'])
                chosen_texts.append(choice.get('text', ''))
        elif strategy == 'all':
            for it in remaining:
                p = it.get('p', default_p)
                if p is None or self._rng.random() < float(p):
                    chosen_names.append(it['name'])
                    chosen_texts.append(it.get('text', ''))
        else:
            for it in remaining:
                p = it.get('p', default_p)
                if p is None:
                    continue
                if self._rng.random() < float(p):
                    chosen_names.append(it['name'])
                    chosen_texts.append(it.get('text', ''))

        return chosen_names, chosen_texts

    def get_A_template(self, question_type: str) -> tuple:
        '''Generate the answer template for a specific question type.
        Args:
            question_type: The type of question to generate an answer for.
        Returns:
            A tuple containing the answer template and a list of chosen optional types.
        '''
        base_template, cfg = self._resolve_template(
            self.a_dict, key=question_type)
        if not base_template:
            # fallback to a_dict['template'] or a generic pattern
            base_template, cfg = self._resolve_template(self.a_dict)

        optional_cfg = cfg.get('optional') or cfg.get('optionals') or {}
        chosen_names, chosen_texts = self._choose_optionals(optional_cfg)

        cot_prompt = cfg.get('cot') if 'cot' in cfg else None
        if self.is_cot:
            cot_prompt = cot_prompt or "Let's think step by step."

        parts: List[str] = []
        if base_template:
            parts.append(base_template)
        if chosen_texts:
            parts.append('\n'.join(chosen_texts))
        if cot_prompt:
            parts.append(str(cot_prompt))

        combined = '\n\n'.join([p for p in parts if p])

        combined = self._apply_wrappers(combined, cfg)
        combined = self._fill_common(
            combined, {'question_type': question_type})

        return combined, chosen_names

    def get_Q_template(self, question_type_prompt: str) -> str:
        '''Generate the question template based on the provided prompt.
        Args:
            question_type_prompt: The prompt describing the question type.
        Returns:
            The question generation template with the question type filled in.
        '''
        base_template, cfg = self._resolve_template(self.q_dict)
        if not base_template:
            base_template = "You are to generate questions of type: {question_type_prompt}."

        text = self._apply_wrappers(base_template, cfg)
        text = self._fill_common(
            text, {'question_type_prompt': question_type_prompt})
        return text
