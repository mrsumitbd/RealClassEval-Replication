
import random


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
        a_conf = self.a_dict.get(question_type, {})
        template = a_conf.get('template', '')
        optionals = a_conf.get('optionals', [])
        chosen_optionals = []
        # If optionals is a dict with weights, sample accordingly
        if isinstance(optionals, dict):
            keys = list(optionals.keys())
            weights = list(optionals.values())
            # Choose one or more optionals based on weights
            chosen = random.choices(keys, weights=weights, k=1)
            chosen_optionals = chosen
        elif isinstance(optionals, list):
            # Choose all, or a random subset, or none, depending on config
            chosen_optionals = optionals
        # Fill in user_name and global_bio if present in template
        template_filled = template.replace('{user_name}', self.user_name).replace(
            '{global_bio}', self.global_bio)
        # Optionally, add COT (chain-of-thought) if is_cot is True and template supports it
        if self.is_cot and '{cot}' in template_filled:
            template_filled = template_filled.replace(
                '{cot}', 'Let\'s think step by step.')
        elif '{cot}' in template_filled:
            template_filled = template_filled.replace('{cot}', '')
        return (template_filled, chosen_optionals)

    def get_Q_template(self, question_type_prompt: str) -> str:
        '''Generate the question template based on the provided prompt.
        Args:
            question_type_prompt: The prompt describing the question type.
        Returns:
            The question generation template with the question type filled in.
        '''
        q_conf = self.q_dict.get(question_type_prompt, {})
        template = q_conf.get('template', '')
        # Fill in user_name and global_bio if present in template
        template_filled = template.replace('{user_name}', self.user_name).replace(
            '{global_bio}', self.global_bio)
        return template_filled
