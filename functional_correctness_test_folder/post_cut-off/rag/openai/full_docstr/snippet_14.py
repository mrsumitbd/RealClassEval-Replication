
class templater:
    """Class for generating templates for question and answer generation.
    This class handles the creation of templates for generating both questions
    and answers based on predefined rules and configurations.
    """

    def __init__(
        self,
        q_dict: dict,
        a_dict: dict,
        user_name: str = "",
        global_bio: str = "",
        is_cot: bool = True,
    ):
        """
        Initialize the templater with question and answer dictionaries.

        Args:
            q_dict: Dictionary containing question type configurations.
            a_dict: Dictionary containing answer type configurations.
            user_name: Name of the user for personalization.
            global_bio: Global biography for context.
            is_cot: Whether to prepend a chain‑of‑thought prefix to answers.
        """
        self.q_dict = q_dict or {}
        self.a_dict = a_dict or {}
        self.user_name = user_name
        self.global_bio = global_bio
        self.is_cot = is_cot

    # --------------------------------------------------------------------- #
    #  Answer template generation
    # --------------------------------------------------------------------- #
    def get_A_template(self, question_type: str) -> tuple:
        """
        Generate the answer template for a specific question type.

        Args:
            question_type: The type of question to generate an answer for.

        Returns:
            A tuple containing the answer template and a list of chosen optional types.
        """
        config = self.a_dict.get(question_type)
        if config is None:
            raise KeyError(
                f"Answer type '{question_type}' not found in a_dict.")

        # Extract template and optional types
        template = config.get("template", "")
        optional = config.get("optional", [])

        # Format placeholders
        template = self._safe_format(
            template,
            user_name=self.user_name,
            global_bio=self.global_bio,
        )

        # Prepend chain‑of‑thought if requested
        if self.is_cot:
            template = f"Chain of thought: {template}"

        return template, optional

    # --------------------------------------------------------------------- #
    #  Question template generation
    # --------------------------------------------------------------------- #
    def get_Q_template(self, question_type_prompt: str) -> str:
        """
        Generate the question template based on the provided prompt.

        Args:
            question_type_prompt: The prompt describing the question type.

        Returns:
            The question generation template with the question type filled in.
        """
        # Try to find a specific template for the prompt
        config = self.q_dict.get(question_type_prompt)

        if config is not None:
            template = config.get("template", "")
        else:
            # Fallback to a default template if available
            default_cfg = self.q_dict.get("default")
            if default_cfg is not None:
                template = default_cfg.get("template", "")
            else:
                # If nothing is defined, use a simple generic template
                template = "Answer the following question: {question_type_prompt}"

        # Format placeholders
        template = self._safe_format(
            template,
            question_type_prompt=question_type_prompt,
            user_name=self.user_name,
            global_bio=self.global_bio,
        )

        return template

    # --------------------------------------------------------------------- #
    #  Utility helpers
    # --------------------------------------------------------------------- #
    @staticmethod
    def _safe_format(template: str, **kwargs) -> str:
        """
        Safely format a template string, leaving placeholders intact if missing.
        """
        try:
            return template.format(**kwargs)
        except KeyError:
            # If a placeholder is missing, leave it unchanged
            return template
