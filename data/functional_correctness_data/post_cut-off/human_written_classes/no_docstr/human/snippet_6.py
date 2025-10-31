import logging
from typing import Any, Dict, List, Optional, Union

class ShadeInfo:

    def __init__(self, id: int=None, name: str='', aspect: str='', icon: str='', descThirdView: str='', contentThirdView: str='', descSecondView: str='', contentSecondView: str='', timelines: List[Dict[str, Any]]=[], confidenceLevel: str=None):
        self.id = id
        self.name = name
        self.aspect = aspect
        self.icon = icon
        self.desc_second_view = descSecondView
        self.desc_third_view = descThirdView
        self.content_third_view = contentThirdView
        self.content_second_view = contentSecondView
        if confidenceLevel:
            self.confidence_level = ConfidenceLevel(confidenceLevel)
        else:
            self.confidence_level = None
        self.timelines = [ShadeTimeline(**timeline) for timeline in timelines]

    def imporve_shade_info(self, improveDesc: str, improveContent: str, improveTimelines: List[Dict[str, Any]]):
        self.desc_third_view = improveDesc
        self.content_third_view = improveContent
        self.timelines.extend([ShadeTimeline.from_raw_format(timeline) for timeline in improveTimelines])

    def add_second_view(self, domainDesc: str, domainContent: str, domainTimeline: List[Dict[str, Any]], *args, **kwargs):
        self.desc_second_view = domainDesc
        self.content_second_view = domainContent
        timelime_dict = {timelime.ref_memory_id: timelime for timelime in self.timelines}
        for timeline in domainTimeline:
            ref_memory_id = timeline.get('refMemoryId', None)
            if not (ref_memory_id and ref_memory_id in timelime_dict):
                logging.error(f'Timeline with refMemoryId {ref_memory_id} already exists, skipping')
                continue
            timelime_dict[ref_memory_id].add_second_view(timeline.get('description', ''))

    def _preview_(self, second_view: bool=False):
        if second_view:
            return f'- **{self.name}**: {self.desc_second_view}'
        return f'- **{self.name}**: {self.desc_third_view}'

    def to_str(self):
        shade_statement = f'---\n**[Name]**: {self.name}\n**[Aspect]**: {self.aspect}\n**[Icon]**: {self.icon}\n'
        shade_statement += f'**[Description]**: \n{self.desc_third_view}\n\n**[Content]**: \n{self.content_third_view}\n'
        shade_statement += '---\n\n[Timelines]:\n'
        for timeline in self.timelines:
            shade_statement += f'- {timeline.create_time}, {timeline.desc_third_view}, {timeline.ref_memory_id}\n'
        return shade_statement

    def to_json(self):
        return {'id': self.id, 'name': self.name, 'aspect': self.aspect, 'icon': self.icon, 'descSecondView': self.desc_second_view, 'descThirdView': self.desc_third_view, 'contentThirdView': self.content_third_view, 'contentSecondView': self.content_second_view, 'confidenceLevel': self.confidence_level if self.confidence_level else None, 'timelines': [timeline.to_json() for timeline in self.timelines]}