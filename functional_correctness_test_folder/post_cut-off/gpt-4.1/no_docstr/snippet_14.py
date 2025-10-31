
class templater:

    def __init__(self, q_dict: dict, a_dict: dict, user_name: str = '', global_bio: str = '', is_cot: bool = True):
        self.q_dict = q_dict
        self.a_dict = a_dict
        self.user_name = user_name
        self.global_bio = global_bio
        self.is_cot = is_cot

    def get_A_template(self, question_type: str) -> tuple:
        # Returns (template, is_cot)
        template = self.a_dict.get(question_type, "")
        return (template, self.is_cot)

    def get_Q_template(self, question_type_prompt: str) -> str:
        template = self.q_dict.get(question_type_prompt, "")
        if self.user_name or self.global_bio:
            prefix = ""
            if self.user_name:
                prefix += f"User: {self.user_name}\n"
            if self.global_bio:
                prefix += f"Bio: {self.global_bio}\n"
            return prefix + template
        return template
