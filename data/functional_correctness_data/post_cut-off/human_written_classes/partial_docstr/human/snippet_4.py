from typing import Dict, Any, List, Optional

class EntityWiki:

    def __init__(self, wikiText: str, monthlyTimelines: List[Dict[str, Any]]):
        self.wiki_text = wikiText
        self.monthly_timelines = [MonthlyTimeline(**monthly_timeline) for monthly_timeline in monthlyTimelines]
        self.max_month_idx = max([monthly_timeline.id for monthly_timeline in self.monthly_timelines]) if self.monthly_timelines else 0

    def to_dict(self) -> Dict[str, Any]:
        """Converts the EntityWiki object to a dictionary.

        Returns:
            Dict[str, Any]: Dictionary representation of the EntityWiki.
        """
        return {'wikiText': self.wiki_text, 'monthlyTimelines': [monthly_timeline.to_dict() for monthly_timeline in self.monthly_timelines]}