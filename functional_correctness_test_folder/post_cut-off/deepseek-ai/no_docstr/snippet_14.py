
class templater:

    def __init__(self, q_dict: dict, a_dict: dict, user_name: str = '', global_bio: str = '', is_cot: bool = True):
        self.q_dict = q_dict
        self.a_dict = a_dict
        self.user_name = user_name
        self.global_bio = global_bio
        self.is_cot = is_cot

    def get_A_template(self, question_type: str) -> tuple:
        if question_type not in self.a_dict:
            raise ValueError(
                f"Question type '{question_type}' not found in answer templates.")
        template = self.a_dict[question_type]
        if self.is_cot:
            return (template, "Let me think step by step.")
        return (template, "")

    def get_Q_template(self, question_type_prompt: str) -> str:
        if question_type_prompt not in self.q_dict:
            raise ValueError(
                f"Question type prompt '{question_type_prompt}' not found in question templates.")
        template = self.q_dict[question_type_prompt]
        if self.user_name:
            template = template.replace("{user_name}", self.user_name)
        if self.global_bio:
            template = template.replace("{global_bio}", self.global_bio)
        return template
