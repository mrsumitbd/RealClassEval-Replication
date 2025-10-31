
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
        self.q_dict = q_dict
        self.a_dict = a_dict
        self.user_name = user_name
        self.global_bio = global_bio
        self.is_cot = is_cot

    def get_A_template(self, question_type: str) -> tuple:
        '''Generate the answer template for a specific question type.
        Args:
            question_type: The type of question to generate an answer for.
        Returns:
            A tuple containing the answer template and a list of chosen optional types.
        '''
        if question_type not in self.a_dict:
            raise KeyError(
                f"Answer type '{question_type}' not found in a_dict")
        entry = self.a_dict[question_type]
        template = entry.get('template', '')
        # Optional types may be a list; choose all if is_cot else empty
        optional_types = entry.get('optional_types', [])
        if not self.is_cot:
            optional_types = []
        return template, optional_types

    def get_Q_template(self, question_type_prompt: str) -> str:
        '''Generate the question template based on the provided prompt.
        Args:
            question_type_prompt: The prompt describing the question type.
        Returns:
            The question generation template with the question type filled in.
        '''
        if question_type_prompt not in self.q_dict:
            raise KeyError(
                f"Question type prompt '{question_type_prompt}' not found in q_dict")
        entry = self.q_dict[question_type_prompt]
        template = entry.get('template', '')
        # Replace placeholders if present
        try:
            template = template.format(
                user_name=self.user_name,
                global_bio=self.global_bio,
                question_type_prompt=question_type_prompt
            )
        except KeyError:
            # If template uses different placeholder names, leave as is
            pass
        return template
