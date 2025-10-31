
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
            raise ValueError("Invalid vulnerability type")

    @staticmethod
    def generate_competitor_mention_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"Competitor Mention Baseline Attacks: Max Goldens - {max_goldens}, Purpose - {purpose}"

    @staticmethod
    def generate_market_manipulation_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"Market Manipulation Baseline Attacks: Max Goldens - {max_goldens}, Purpose - {purpose}"

    @staticmethod
    def generate_discreditation_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"Discreditation Baseline Attacks: Max Goldens - {max_goldens}, Purpose - {purpose}"

    @staticmethod
    def generate_confidential_strategies_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return f"Confidential Strategies Baseline Attacks: Max Goldens - {max_goldens}, Purpose - {purpose}"
