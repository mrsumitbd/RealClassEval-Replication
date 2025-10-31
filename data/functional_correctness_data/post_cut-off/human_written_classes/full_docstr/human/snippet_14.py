import random

class templater:
    """Class for generating templates for question and answer generation.

    This class handles the creation of templates for generating both questions
    and answers based on predefined rules and configurations.
    """

    def __init__(self, q_dict: dict, a_dict: dict, user_name: str='', global_bio: str='', is_cot: bool=True):
        """Initialize the templater with question and answer dictionaries.

        Args:
            q_dict: Dictionary containing question type configurations.
            a_dict: Dictionary containing answer type configurations.
            user_name: Name of the user for personalization.
            global_bio: Global biography for context.
        """
        self.a_dict = a_dict
        self.q_dict = q_dict
        self.user_name = user_name
        self.global_bio = global_bio
        self.is_cot = is_cot
        self.shot1, self.cot_shot1 = (SHOT_1, COT_SHOT_1)
        self.shot2, self.cot_shot2 = (SHOT_2, COT_SHOT_2)
        self.a_temp, self.a_cot_temp = (A_GENERATE_TEMPLATE, A_GENERATE_COT_TEMPLATE)

    def get_A_template(self, question_type: str) -> tuple:
        """Generate the answer template for a specific question type.

        Args:
            question_type: The type of question to generate an answer for.

        Returns:
            A tuple containing the answer template and a list of chosen optional types.
        """
        templ = self.a_cot_temp if self.is_cot else self.a_temp
        answer_rule = ''
        required_type = self.q_dict[question_type]['requiredAnswerTypes']
        optional_type = self.q_dict[question_type]['optionalAnswerTypes']
        if required_type:
            answer_rule = 'The required expressions to be included in the response:\n'
            for ind, answer_type in enumerate(required_type):
                sub_prompt = self.a_dict[answer_type]['prompt']
                answer_rule += f'{ind + 1}. {sub_prompt}\n'
        if optional_type:
            k = random.randint(1, len(optional_type))
            chosen_optional_type = random.sample(optional_type, k)
        else:
            chosen_optional_type = []
        if chosen_optional_type:
            answer_rule += 'The optional, combinable response expression:\n'
            for ind, answer_type in enumerate(chosen_optional_type):
                sub_prompt = self.a_dict[answer_type]['prompt']
                answer_rule += f'{ind + 1}. {sub_prompt}\n'
        templ = templ.replace('__answer_rule__', answer_rule)
        bio = ''
        status_bio_flag = False
        global_bio_flag = False
        for type in chosen_optional_type:
            extra_info = self.a_dict[type]['extraInfo']
            if 'statusBio' in extra_info:
                status_bio_flag = True
                break
            if 'globalBio' in extra_info:
                global_bio_flag = True
                break
        if status_bio_flag:
            bio += f'The recent status of {self.user_name} is:\n\n{self.status_bio}\n'
        if global_bio_flag:
            bio += f'The user profile of {self.user_name} is:\n\n{self.global_bio}\n'
        if bio:
            bio += 'You may refer to the above information when responding, but do not overuse it.'
            templ = templ.replace('# Guidelines #', f'# Guidelines #\n{bio}')
        if question_type == 'global':
            if self.is_cot:
                tmp = random.choice([self.cot_shot1, self.cot_shot2, self.cot_shot2])
            else:
                tmp = random.choice([self.shot1, self.shot2, self.shot2])
            templ += f'# Example Output #\n{tmp}'
        return (templ, chosen_optional_type)

    def get_Q_template(self, question_type_prompt: str) -> str:
        """Generate the question template based on the provided prompt.

        Args:
            question_type_prompt: The prompt describing the question type.

        Returns:
            The question generation template with the question type filled in.
        """
        return Q_GENERATE_TEMPLATE.replace('__question_type__', question_type_prompt)