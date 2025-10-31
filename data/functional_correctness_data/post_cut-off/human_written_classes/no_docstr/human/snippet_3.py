from typing import Any, Dict, List, Optional, Union

class Bio:

    def __init__(self, contentThirdView: str='', content: str='', summaryThirdView: str='', summary: str='', attributeList: List[Dict[str, Any]]=[], shadesList: List[Dict[str, Any]]=[]):
        self.content_third_view = contentThirdView
        self.content_second_view = content
        self.summary_third_view = summaryThirdView
        self.summary_second_view = summary
        self.attribute_list = sorted([AttributeInfo(**attribute) for attribute in attributeList], key=lambda x: CONFIDENCE_LEVELS_INT[x.confidence_level], reverse=True)
        self.shades_list = sorted([ShadeInfo(**shade) for shade in shadesList], key=lambda x: len(x.timelines), reverse=True)

    def to_str(self) -> str:
        global_bio_statement = ''
        if self.is_raw_bio():
            global_bio_statement += f'**[Origin Analysis]**\n{self.summary_third_view}\n'
        global_bio_statement += f'\n**[Current Shades]**\n'
        for shade in self.shades_list:
            global_bio_statement += shade.to_str()
            global_bio_statement += '\n==============\n'
        return global_bio_statement

    def complete_content(self, second_view: bool=False) -> str:
        interests_preference_field = "\n### User's Interests and Preferences ###\n" + '\n'.join([shade._preview_(second_view) for shade in self.shades_list])
        if not second_view:
            conclusion_field = '\n### Conclusion ###\n' + self.summary_third_view
        else:
            conclusion_field = '\n### Conclusion ###\n' + self.summary_second_view
        return f'## Comprehensive Analysis Report ##\n{interests_preference_field}\n{conclusion_field}'

    def is_raw_bio(self) -> bool:
        if not self.content_third_view and (not self.summary_third_view):
            return True
        return False

    def to_json(self) -> Dict[str, Any]:
        return {'contentThirdView': self.content_third_view, 'content': self.content_second_view, 'summaryThirdView': self.summary_third_view, 'summary': self.summary_second_view, 'shadesList': [shade.to_json() for shade in self.shades_list]}