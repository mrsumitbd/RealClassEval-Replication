
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
        # If optionals is a dict, select randomly or by rule
        if isinstance(optionals, dict):
            for key, opts in optionals.items():
                if isinstance(opts, list) and opts:
                    chosen = random.choice(opts)
                    chosen_optionals.append((key, chosen))
        elif isinstance(optionals, list):
            chosen_optionals = optionals
        # Fill in user_name and global_bio if present in template
        template_filled = template.replace('{user_name}', self.user_name).replace(
            '{global_bio}', self.global_bio)
        # Optionally, add chain-of-thought if is_cot is True and template supports it
        if self.is_cot and '{chain_of_thought}' in template_filled:
            template_filled = template_filled.replace(
                '{chain_of_thought}', 'Let\'s think step by step.')
        elif '{chain_of_thought}' in template_filled:
            template_filled = template_filled.replace('{chain_of_thought}', '')
        return template_filled, chosen_optionals

    def get_Q_template(self, question_type_prompt: str) -> str:
        '''Generate the question template based on the provided prompt.
        Args:
            question_type_prompt: The prompt describing the question type.
        Returns:
            The question generation template with the question type filled in.
        '''
        # Find the template for the given question type prompt
        q_conf = self.q_dict.get(question_type_prompt, {})
        template = q_conf.get('template', '')
        # Fill in user_name and global_bio if present in template
        template_filled = template.replace('{user_name}', self.user_name).replace(
            '{global_bio}', self.global_bio)
        return template_filled
