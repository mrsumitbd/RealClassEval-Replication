from typing import Optional, Any


class ToxicityTemplate:
    @staticmethod
    def _normalize_type(vulnerability_type: Any) -> str:
        name = getattr(vulnerability_type, "name", None)
        if isinstance(name, str):
            return name.lower()
        if isinstance(vulnerability_type, str):
            return vulnerability_type.lower()
        return str(vulnerability_type).lower()

    @staticmethod
    def _validate_max_goldens(max_goldens: int) -> int:
        if not isinstance(max_goldens, int):
            raise TypeError("max_goldens must be an integer")
        if max_goldens < 0:
            raise ValueError("max_goldens must be non-negative")
        return max_goldens

    @staticmethod
    def _format_purpose(purpose: Optional[str]) -> str:
        return purpose.strip() if isinstance(purpose, str) and purpose.strip() else "unspecified"

    @staticmethod
    def _build_placeholders(category: str, max_goldens: int, purpose: Optional[str]) -> str:
        ToxicityTemplate._validate_max_goldens(max_goldens)
        if max_goldens == 0:
            return ""
        p = ToxicityTemplate._format_purpose(purpose)
        lines = []
        for i in range(1, max_goldens + 1):
            lines.append(
                f"[Example {i}] Category: {category}; Purpose: {p}; Content: [REDACTED - toxic content is not generated]"
            )
        return "\n".join(lines)

    @staticmethod
    def generate_baseline_attacks(vulnerability_type: Any, max_goldens: int, purpose: Optional[str]) -> str:
        vt = ToxicityTemplate._normalize_type(vulnerability_type)
        if "insult" in vt:
            return ToxicityTemplate.generate_insults_baseline_attacks(max_goldens, purpose)
        if "profan" in vt or "swear" in vt or "obscen" in vt:
            return ToxicityTemplate.generate_profanity_baseline_attacks(max_goldens, purpose)
        if "threat" in vt or "violence" in vt:
            return ToxicityTemplate.generate_threats_baseline_attacks(max_goldens, purpose)
        if "mock" in vt or "taunt" in vt or "derog" in vt:
            return ToxicityTemplate.generate_mockery_baseline_attacks(max_goldens, purpose)
        return ToxicityTemplate._build_placeholders("general-toxicity", max_goldens, purpose)

    @staticmethod
    def generate_insults_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return ToxicityTemplate._build_placeholders("insults", max_goldens, purpose)

    @staticmethod
    def generate_profanity_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return ToxicityTemplate._build_placeholders("profanity", max_goldens, purpose)

    @staticmethod
    def generate_threats_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return ToxicityTemplate._build_placeholders("threats", max_goldens, purpose)

    @staticmethod
    def generate_mockery_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        return ToxicityTemplate._build_placeholders("mockery", max_goldens, purpose)
