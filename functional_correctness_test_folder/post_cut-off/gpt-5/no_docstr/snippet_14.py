class templater:
    class _SafeDict(dict):
        def __missing__(self, key):
            return ""

    def __init__(self, q_dict: dict, a_dict: dict, user_name: str = "", global_bio: str = "", is_cot: bool = True):
        self.q_dict = q_dict or {}
        self.a_dict = a_dict or {}
        self.user_name = user_name or ""
        self.global_bio = global_bio or ""
        self.is_cot = bool(is_cot)

    def _format(self, template: str) -> str:
        if not isinstance(template, str):
            return ""
        return template.format_map(self._SafeDict(user_name=self.user_name, global_bio=self.global_bio))

    def get_A_template(self, question_type: str) -> tuple:
        tpl = self.a_dict.get(question_type, None)

        if isinstance(tpl, dict):
            if self.is_cot and "cot" in tpl:
                chosen = tpl["cot"]
                return (self._format(chosen), True)
            if not self.is_cot and "no_cot" in tpl:
                chosen = tpl["no_cot"]
                return (self._format(chosen), False)
            # Fallbacks within dict
            if "default" in tpl:
                chosen = tpl["default"]
                return (self._format(chosen), self.is_cot)
            # Arbitrary first value as last resort
            for v in tpl.values():
                return (self._format(v if isinstance(v, str) else ""), self.is_cot)
            return ("", self.is_cot)

        if isinstance(tpl, str):
            return (self._format(tpl), self.is_cot)

        # Global defaults
        if self.is_cot:
            default = "Think step by step and provide your reasoning, then deliver a concise answer."
            return (self._format(default), True)
        else:
            default = "Provide a concise, direct answer without revealing internal reasoning."
            return (self._format(default), False)

    def get_Q_template(self, question_type_prompt: str) -> str:
        tpl = self.q_dict.get(question_type_prompt, None)
        if isinstance(tpl, str):
            return self._format(tpl)
        if isinstance(tpl, dict):
            # If dict provided, try common keys or any string value
            for key in ("template", "default", "prompt"):
                if key in tpl and isinstance(tpl[key], str):
                    return self._format(tpl[key])
            for v in tpl.values():
                if isinstance(v, str):
                    return self._format(v)
        # Default question prompt
        default = "Please answer the following question for {user_name}. {global_bio}"
        return self._format(default)
