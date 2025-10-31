
class Templater:
    def __init__(self, q_dict: dict, a_dict: dict, user_name: str = '', global_bio: str = '', is_cot: bool = True):
        self.q_dict = q_dict
        self.a_dict = a_dict
        self.user_name = user_name
        self.global_bio = global_bio
        self.is_cot = is_cot

    def get_A_template(self, question_type: str) -> tuple:
        answer_template = self.a_dict.get(question_type, ("", ""))
        if self.is_cot:
            return answer_template
        else:
            return (answer_template[0], "")

    def get_Q_template(self, question_type_prompt: str) -> str:
        return self.q_dict.get(question_type_prompt, "")
