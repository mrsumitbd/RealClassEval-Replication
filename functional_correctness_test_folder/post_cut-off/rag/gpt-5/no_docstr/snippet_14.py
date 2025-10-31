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
        self.q_dict = q_dict or {}
        self.a_dict = a_dict or {}
        self.user_name = user_name or ''
        self.global_bio = global_bio or ''
        self.is_cot = bool(is_cot)

        # Default question template if none provided
        self._q_base_template = (
            self.q_dict.get('template')
            or self.q_dict.get('base_template')
            or "Generate a {question_type} question tailored for {user_name}. "
               "Use the following context if relevant: {global_bio}"
        )

        # Optional prefix/suffix for question generation
        self._q_prefix = self.q_dict.get('prefix', '')
        self._q_suffix = self.q_dict.get('suffix', '')

        # Per-type overrides for question templates
        self._q_per_type = self.q_dict.get('per_type', {}) or {}

        # Default answer configuration fallbacks
        self._a_default = self.a_dict.get('default', {})

    def _safe_format(self, template: str, **kwargs) -> str:
        class _SafeDict(dict):
            def __missing__(self, key):
                return '{' + key + '}'
        return template.format_map(_SafeDict(**kwargs))

    def _weighted_sample_without_replacement(self, items, weights, k):
        import random
        if k <= 0 or not items:
            return []
        k = min(k, len(items))
        population = list(items)
        w = list(weights)
        chosen = []
        for _ in range(k):
            total = sum(w)
            if total <= 0:
                # fall back to uniform if all weights are zero/non-positive
                idx = random.randrange(len(population))
            else:
                r = random.random() * total
                acc = 0.0
                idx = 0
                for i, weight in enumerate(w):
                    acc += max(weight, 0.0)
                    if r <= acc:
                        idx = i
                        break
            chosen.append(population.pop(idx))
            w.pop(idx)
        return chosen

    def get_A_template(self, question_type: str) -> tuple:
        '''Generate the answer template for a specific question type.
        Args:
            question_type: The type of question to generate an answer for.
        Returns:
            A tuple containing the answer template and a list of chosen optional types.
        '''
        import random

        spec = self.a_dict.get(question_type, self._a_default) or {}

        # Gather required and optional sections
        required = list(spec.get('required', spec.get(
            'required_types', []))) or ['answer']
        optional_all = list(
            spec.get('optional', spec.get('optional_types', []))) or []

        # Determine how many optional sections to include
        num_opt = spec.get('num_optional', spec.get('choose_optional', None))
        if isinstance(num_opt, (list, tuple)) and len(num_opt) == 2:
            min_opt, max_opt = num_opt
        else:
            min_opt = spec.get(
                'min_optional', 0 if num_opt is None else int(num_opt))
            max_opt = spec.get('max_optional', len(
                optional_all) if num_opt is None else int(num_opt))

        min_opt = max(0, int(min_opt))
        max_opt = max(min_opt, int(max_opt))
        max_opt = min(max_opt, len(optional_all))

        # Weights for optional selection
        weights_map = spec.get('optional_weights', {}) or {}
        weights = [float(weights_map.get(opt, 1.0)) for opt in optional_all]

        # Selection strategy
        strategy = spec.get('optional_strategy',
                            'random' if optional_all else 'none')
        if strategy == 'none':
            chosen_optional = []
        elif strategy == 'all':
            chosen_optional = optional_all[:]
        else:
            k = random.randint(min_opt, max_opt) if max_opt > 0 else 0
            if k <= 0:
                chosen_optional = []
            else:
                chosen_optional = self._weighted_sample_without_replacement(
                    optional_all, weights, k)

        # Build template
        # If a raw template is provided, format and return
        raw_template = spec.get('template')
        context = {
            'question_type': question_type,
            'user_name': self.user_name or 'the user',
            'global_bio': self.global_bio,
            'required': required,
            'optional': chosen_optional,
            'all_optional': optional_all,
        }
        use_cot = spec.get('is_cot', self.is_cot)
        cot_instruction = spec.get('cot_instruction') or (
            "Think step by step and reason through the problem before giving the final answer."
            if use_cot else ""
        )

        if raw_template:
            final = self._safe_format(
                raw_template,
                **context,
                cot_instruction=cot_instruction
            ).strip()
            return final, chosen_optional

        # Otherwise, synthesize a template
        format_type = (spec.get('format') or 'text').lower()

        header = spec.get(
            'header') or f"Provide a response to a {question_type} question for {context['user_name']}."
        if self.global_bio:
            header += f" Use the following context if helpful: {self.global_bio}"

        requirements_lines = []
        for r in required:
            instruction = spec.get('sections', {}).get(
                r) or f"Include a clear and concise {r}."
            requirements_lines.append(f"- {instruction}")

        optional_lines = []
        for opt in chosen_optional:
            instruction = spec.get('sections', {}).get(
                opt) or f"Include {opt} if relevant."
            optional_lines.append(f"- {instruction}")

        if format_type == 'json':
            keys = required + chosen_optional
            keys_line = ', '.join(f'"{k}"' for k in keys)
            body_lines = [
                header,
                "Output strictly in JSON with the following keys:",
                f"[{keys_line}]",
            ]
            if cot_instruction:
                body_lines.append(cot_instruction)
            body_lines.append("Do not include additional keys.")
            template = "\n".join(body_lines)
            return template.strip(), chosen_optional

        # text format (default)
        body = [
            header,
            "Provide the following:",
            *requirements_lines,
        ]
        if optional_lines:
            body.append("Optionally include:")
            body.extend(optional_lines)
        if cot_instruction:
            body.append(cot_instruction)
        closing = spec.get(
            'closing', "If information is missing, state reasonable assumptions.")
        if closing:
            body.append(closing)

        template = "\n".join(body).strip()
        return template, chosen_optional

    def get_Q_template(self, question_type_prompt: str) -> str:
        '''Generate the question template based on the provided prompt.
        Args:
            question_type_prompt: The prompt describing the question type.
        Returns:
            The question generation template with the question type filled in.
        '''
        # Per-type override if present
        per_type_template = None
        if isinstance(self._q_per_type, dict):
            per_type_template = self._q_per_type.get(question_type_prompt)

        template = per_type_template or self._q_base_template
        parts = [self._q_prefix, template, self._q_suffix]
        combined = " ".join(p for p in parts if p).strip()

        context = {
            'question_type': question_type_prompt,
            'user_name': self.user_name or 'the user',
            'global_bio': self.global_bio,
        }
        return self._safe_format(combined, **context).strip()
