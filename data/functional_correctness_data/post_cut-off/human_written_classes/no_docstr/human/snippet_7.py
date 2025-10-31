from typing import Any, Dict, List, Optional, Union
import json

class ShadeMergeInfo:

    def __init__(self, id: int=None, name: str='', aspect: str='', icon: str='', desc_third_view: str='', content_third_view: str='', desc_second_view: str='', content_second_view: str='', cluster_info: Optional[Dict[str, Any]]=None):
        self.id = id
        self.name = name
        self.aspect = aspect
        self.icon = icon
        self.desc_second_view = desc_second_view
        self.desc_third_view = desc_third_view
        self.content_third_view = content_third_view
        self.content_second_view = content_second_view
        self.cluster_info = cluster_info

    def improve_shade_info(self, improveDesc: str, improveContent: str):
        self.desc_third_view = improveDesc
        self.content_third_view = improveContent

    def add_second_view(self, domainDesc: str, domainContent: str):
        self.desc_second_view = domainDesc
        self.content_second_view = domainContent

    def _preview_(self, second_view: bool=False):
        if second_view:
            return f'- **{self.name}**: {self.desc_second_view}'
        return f'- **{self.name}**: {self.desc_third_view}'

    def to_str(self):
        shade_statement = f'---\n**[Name]**: {self.name}\n**[Aspect]**: {self.aspect}\n**[Icon]**: {self.icon}\n'
        shade_statement += f'**[Description]**: \n{self.desc_third_view}\n\n**[Content]**: \n{self.content_third_view}\n'
        shade_statement += '---\n\n'
        if self.cluster_info:
            shade_statement += f'**[Cluster Info]**: \n{json.dumps(self.cluster_info, indent=2)}\n'
        return shade_statement

    def to_json(self):
        return {'id': self.id, 'name': self.name, 'aspect': self.aspect, 'icon': self.icon, 'descSecondView': self.desc_second_view, 'descThirdView': self.desc_third_view, 'contentThirdView': self.content_third_view, 'contentSecondView': self.content_second_view, 'clusterInfo': self.cluster_info}