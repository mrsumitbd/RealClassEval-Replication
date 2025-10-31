
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
        answer_config = self.a_dict.get(question_type, {})
        template = answer_config.get('template', '')
        optional_types = answer_config.get('optional_types', [])

        if self.is_cot:
            template = f"{template}\n\nLet's think step by step."

        return (template, optional_types)

    def get_Q_template(self, question_type_prompt: str) -> str:
        '''Generate the question template based on the provided prompt.
        Args:
            question_type_prompt: The prompt describing the question type.
        Returns:
            The question generation template with the question type filled in.
        '''
        question_config = self.q_dict.get(question_type_prompt, {})
        template = question_config.get('template', '')

        if self.user_name:
            template = template.replace('{user_name}', self.user_name)
        if self.global_bio:
            template = template.replace('{global_bio}', self.global_bio)

        return template
