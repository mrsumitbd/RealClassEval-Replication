
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
        self.user_name = user_name
        self.global_bio = global_bio
        self.is_cot = is_cot

    def _safe_format(self, template: str, **kwargs) -> str:
        '''Format a template string safely, leaving unknown placeholders unchanged.'''
        try:
            return template.format(**kwargs)
        except KeyError:
            # Replace missing keys with empty string
            missing = {k: '' for k in kwargs if k not in template}
            return template.format(**missing)

    def get_A_template(self, question_type: str) -> tuple:
        '''Generate the answer template for a specific question type.
        Args:
            question_type: The type of question to generate an answer for.
        Returns:
            A tuple containing the answer template and a list of chosen optional types.
        '''
        entry = self.a_dict.get(question_type)
        if entry is None:
            # Fallback: no template found
            return ('', [])
        # Entry can be a string or a dict
        if isinstance(entry, str):
            template = entry
            optional = []
        elif isinstance(entry, dict):
            template = entry.get('template', '')
            optional = entry.get('optional', [])
        else:
            template = ''
            optional = []

        # Personalise the template
        template = self._safe_format(template,
                                     user_name=self.user_name,
                                     global_bio=self.global_bio,
                                     is_cot=self.is_cot)
        return (template, optional)

    def get_Q_template(self, question_type_prompt: str) -> str:
        '''Generate the question template based on the provided prompt.
        Args:
            question_type_prompt: The prompt describing the question type.
        Returns:
            The question generation template with the question type filled in.
        '''
        template = self.q_dict.get(question_type_prompt, '')
        if not template:
            return ''
        # Personalise the template
        template = self._safe_format(template,
                                     user_name=self.user_name,
                                     global_bio=self.global_bio,
                                     is_cot=self.is_cot)
        return template
