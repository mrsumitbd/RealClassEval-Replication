
class templater:

    def __init__(self, q_dict: dict, a_dict: dict, user_name: str = '', global_bio: str = '', is_cot: bool = True):
        self.q_dict = q_dict
        self.a_dict = a_dict
        self.user_name = user_name
        self.global_bio = global_bio
        self.is_cot = is_cot

    def get_A_template(self, question_type: str) -> tuple:
        if question_type in self.a_dict:
            return self.a_dict[question_type]
        return ("", "")

    def get_Q_template(self, question_type_prompt: str) -> str:
        if question_type_prompt in self.q_dict:
            return self.q_dict[question_type_prompt]
        return ""
