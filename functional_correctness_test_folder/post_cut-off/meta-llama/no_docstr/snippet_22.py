
from typing import Tuple, Dict, List


class DocumentAnalyzer:

    def analyze_document_type(self, content: str) -> Tuple[str, float]:
        indicators = {
            "technical": ["algorithm", "data structure", "code"],
            "non-technical": ["management", "business", "marketing"]
        }
        scores = {}
        for doc_type, patterns in indicators.items():
            scores[doc_type] = self._detect_pattern_score(content, patterns)
        max_score_doc_type = max(scores, key=scores.get)
        return max_score_doc_type, scores[max_score_doc_type]

    def _calculate_weighted_score(self, content: str, indicators: Dict[str, List[str]]) -> float:
        score = 0.0
        for indicator, patterns in indicators.items():
            score += self._detect_pattern_score(content, patterns)
        return score / len(indicators)

    def _detect_pattern_score(self, content: str, patterns: List[str]) -> float:
        score = 0.0
        for pattern in patterns:
            score += content.lower().count(pattern.lower())
        return score / len(patterns) if patterns else 0.0

    def detect_segmentation_strategy(self, content: str, doc_type: str) -> str:
        if doc_type == "technical":
            algorithm_density = self._calculate_algorithm_density(content)
            if algorithm_density > 0.5:
                return "detailed"
            else:
                return "general"
        else:
            concept_complexity = self._calculate_concept_complexity(content)
            implementation_detail_level = self._calculate_implementation_detail_level(
                content)
            if concept_complexity > 0.5 and implementation_detail_level > 0.5:
                return "detailed"
            else:
                return "general"

    def _calculate_algorithm_density(self, content: str) -> float:
        algorithm_indicators = ["algorithm", "data structure", "complexity"]
        return self._detect_pattern_score(content, algorithm_indicators)

    def _calculate_concept_complexity(self, content: str) -> float:
        complexity_indicators = ["complex", "difficult", "challenging"]
        return self._detect_pattern_score(content, complexity_indicators)

    def _calculate_implementation_detail_level(self, content: str) -> float:
        detail_indicators = ["implementation", "code", "example"]
        return self._detect_pattern_score(content, detail_indicators)
