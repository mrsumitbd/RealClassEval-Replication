
from typing import Optional


class CompetitionType:
    COMPETITOR_MENTION = "competitor_mention"
    MARKET_MANIPULATION = "market_manipulation"
    DISCREDITATION = "discreditation"
    CONFIDENTIAL_STRATEGIES = "confidential_strategies"


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
            return "Unknown vulnerability type"

    @staticmethod
    def generate_competitor_mention_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"Generating competitor mention baseline attacks with max goldens: {max_goldens} for purpose: {purpose}"

    @staticmethod
    def generate_market_manipulation_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"Generating market manipulation baseline attacks with max goldens: {max_goldens} for purpose: {purpose}"

    @staticmethod
    def generate_discreditation_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"Generating discreditation baseline attacks with max goldens: {max_goldens} for purpose: {purpose}"

    @staticmethod
    def generate_confidential_strategies_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"Generating confidential strategies baseline attacks with max goldens: {max_goldens} for purpose: {purpose}"
