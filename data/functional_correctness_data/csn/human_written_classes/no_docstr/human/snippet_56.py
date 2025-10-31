import re

class RegexpMatcher:

    def __init__(self, question):
        self.question = question

    def __call__(self, template):
        res = re.findall(template['template_regexp'], self.question)
        found_template = []
        if res:
            found_template.append((res[0], template))
        return found_template