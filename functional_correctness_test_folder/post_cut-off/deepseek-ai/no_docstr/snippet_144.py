
from typing import Optional
from enum import Enum


class CompetitionType(Enum):
    COMPETITOR_MENTION = 1
    MARKET_MANIPULATION = 2
    DISCREDITATION = 3
    CONFIDENTIAL_STRATEGIES = 4


class CompetitionTemplate:

    @staticmethod
    def generate_baseline_attacks(vulnerability_type: CompetitionType, max_goldens: int, purpose: Optional[str]) -> str:
        if vulnerability_type == CompetitionType.COMPETITOR_MENTION:
            return CompetitionTemplate.generate_competitor_mention_baseline_attacks(max_goldens, purpose)
        elif vulnerability_type == CompetitionType.MARKET_MANIPULATION:
            return CompetitionTemplate.generate_market_manipulation_baseline_attacks(max_goldens, purpose)
        elif vulnerability_type == CompetitionType.DISCREDITATION:
            return CompetitionTemplate.generate_discreditation_baseline_attacks(max_goldens, purpose)
        elif vulnerability_type == CompetitionType.CONFIDENTIAL_STRATEGIES:
            return CompetitionTemplate.generate_confidential_strategies_baseline_attacks(max_goldens, purpose)
        else:
            return ""

    @staticmethod
    def generate_competitor_mention_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"competitor_mention_baseline_attacks_{max_goldens}_{purpose if purpose else 'default'}"

    @staticmethod
    def generate_market_manipulation_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"market_manipulation_baseline_attacks_{max_goldens}_{purpose if purpose else 'default'}"

    @staticmethod
    def generate_discreditation_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"discreditation_baseline_attacks_{max_goldens}_{purpose if purpose else 'default'}"

    @staticmethod
    def generate_confidential_strategies_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"confidential_strategies_baseline_attacks_{max_goldens}_{purpose if purpose else 'default'}"
