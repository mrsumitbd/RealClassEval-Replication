
class templater:
    """
    A simple templating helper that retrieves question and answer templates
    from provided dictionaries and formats them with optional user information.
    """

    def __init__(self, q_dict: dict, a_dict: dict, user_name: str = '', global_bio: str = '', is_cot: bool = True):
        """
        Parameters
        ----------
        q_dict : dict
            Dictionary mapping question type identifiers to question templates.
        a_dict : dict
            Dictionary mapping question type identifiers to answer templates.
        user_name : str, optional
            Name of the user to be inserted into templates.
        global_bio : str, optional
            Global bio or context to be inserted into templates.
        is_cot : bool, optional
            Flag indicating whether chain‑of‑thought should be used for answers.
        """
        self.q_dict = q_dict
        self.a_dict = a_dict
        self.user_name = user_name
        self.global_bio = global_bio
        self.is_cot = is_cot

    def _safe_format(self, template: str) -> str:
        """
        Safely format a template string with available attributes.
        Missing placeholders are left unchanged.
        """
        if not template:
            return ''
        # Build a mapping that returns the placeholder unchanged if missing

        class Default(dict):
            def __missing__(self, key):
                return '{' + key + '}'
        mapping = Default(user_name=self.user_name, global_bio=self.global_bio)
        try:
            return template.format_map(mapping)
        except Exception:
            # Fallback: return the raw template if formatting fails
            return template

    def get_A_template(self, question_type: str) -> tuple:
        """
        Retrieve the answer template for a given question type.

        Returns
        -------
        tuple
            (formatted_template, is_cot_flag)
            If the question type is not found, returns ('', False).
        """
        raw_template = self.a_dict.get(question_type, '')
        formatted = self._safe_format(raw_template)
        return (formatted, self.is_cot)

    def get_Q_template(self, question_type_prompt: str) -> str:
        """
        Retrieve the question template for a given question type prompt.

        Returns
        -------
        str
            The formatted question template. If not found, returns an empty string.
        """
        raw_template = self.q_dict.get(question_type_prompt, '')
        return self._safe_format(raw_template)
