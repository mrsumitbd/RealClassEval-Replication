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

        # Pre-resolve question template defaults
        self._q_template = (
            self.q_dict.get('template')
            or self.q_dict.get('base_template')
            or 'Generate a {question_type} question. Personalize for {user_name}. Context: {global_bio}.'
        )

        # Pre-resolve answer template defaults
        self._a_default_template = (
            self.a_dict.get('template')
            or self.a_dict.get('base_template')
            or (
                'Task: Answer a {question_type} question.\n'
                '{cot}\n'
                '{optional_sections}\n'
                'Personalize for {user_name}. Context: {global_bio}.'
            )
        )
        # Optional overrides for cot messaging
        self._a_cot_true = self.a_dict.get(
            'cot_true',
            'Provide a detailed, step-by-step reasoning (chain-of-thought) before the final answer.'
        )
        self._a_cot_false = self.a_dict.get(
            'cot_false',
            'Provide a concise solution, showing only essential steps, followed by the final answer.'
        )

        # Per-type configurations (optional)
        self._a_types = self.a_dict.get('types') or {}

    def _format(self, template: str, **kwargs) -> str:
        # Safe str.format that ignores missing keys
        class SafeDict(dict):
            def __missing__(self, key):
                return '{' + key + '}'
        return template.format_map(SafeDict(**kwargs))

    def _choose_optionals(self, opt_cfg) -> list:
        # Supports:
        # - list -> choose first k (k from a_dict['optional_choose'] or all)
        # - dict with keys: 'pool': list, 'choose': int
        # - dict with arbitrary keys -> choose all keys
        if not opt_cfg:
            return []
        # If list
        if isinstance(opt_cfg, list):
            k = self.a_dict.get('optional_choose')
            if isinstance(k, int) and k >= 0:
                return opt_cfg[:k]
            return list(opt_cfg)
        # If dict with 'pool'
        if isinstance(opt_cfg, dict) and 'pool' in opt_cfg:
            pool = opt_cfg.get('pool') or []
            choose = opt_cfg.get('choose')
            if isinstance(choose, int) and choose >= 0:
                return pool[:choose]
            return list(pool)
        # If dict arbitrary -> choose all keys
        if isinstance(opt_cfg, dict):
            return list(opt_cfg.keys())
        # Fallback
        return []

    def get_A_template(self, question_type: str) -> tuple:
        '''Generate the answer template for a specific question type.
        Args:
            question_type: The type of question to generate an answer for.
        Returns:
            A tuple containing the answer template and a list of chosen optional types.
        '''
        qt_cfg = self._a_types.get(question_type) if isinstance(
            self._a_types, dict) else None

        # Template selection precedence: per-type template -> global template -> default
        template_str = (
            (qt_cfg.get('template') if isinstance(qt_cfg, dict) else None)
            or self._a_default_template
        )

        # Determine CoT directive
        cot_text = self._a_cot_true if self.is_cot else self._a_cot_false

        # Optional sections determination
        opt_cfg = None
        if isinstance(qt_cfg, dict) and 'optional' in qt_cfg:
            opt_cfg = qt_cfg.get('optional')
        elif 'optional' in self.a_dict:
            opt_cfg = self.a_dict.get('optional')

        chosen_optionals = self._choose_optionals(opt_cfg)

        # Render optional sections string if template expects it
        optional_sections_str = ''
        if '{optional_sections}' in template_str or '{optional}' in template_str:
            if chosen_optionals:
                optional_sections_str = 'Include the following optional elements: ' + \
                    ', '.join(chosen_optionals) + '.'
            else:
                optional_sections_str = ''

        rendered = self._format(
            template_str,
            question_type=question_type,
            user_name=self.user_name,
            global_bio=self.global_bio,
            cot=cot_text,
            optional_sections=optional_sections_str,
            optional=optional_sections_str,
        )
        return rendered, chosen_optionals

    def get_Q_template(self, question_type_prompt: str) -> str:
        '''Generate the question template based on the provided prompt.
        Args:
            question_type_prompt: The prompt describing the question type.
        Returns:
            The question generation template with the question type filled in.
        '''
        # Allow per-type override if provided under q_dict['types']
        q_types = self.q_dict.get('types')
        if isinstance(q_types, dict) and question_type_prompt in q_types:
            tmpl = q_types[question_type_prompt].get(
                'template') or q_types[question_type_prompt].get('base_template')
            if tmpl:
                return self._format(
                    tmpl,
                    question_type=question_type_prompt,
                    user_name=self.user_name,
                    global_bio=self.global_bio,
                )

        return self._format(
            self._q_template,
            question_type=question_type_prompt,
            user_name=self.user_name,
            global_bio=self.global_bio,
        )
