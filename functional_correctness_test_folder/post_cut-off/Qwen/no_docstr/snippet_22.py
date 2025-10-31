
from typing import Tuple, Dict, List


class DocumentAnalyzer:

    def analyze_document_type(self, content: str) -> Tuple[str, float]:
        indicators = {
            "academic": ["research", "literature", "theoretical"],
            "technical": ["algorithm", "implementation", "code"],
            "news": ["report", "breaking", "latest"],
            "fiction": ["character", "plot", "setting"]
        }
        scores = {doc_type: self._calculate_weighted_score(
            content, {doc_type: patterns}) for doc_type, patterns in indicators.items()}
        best_match = max(scores, key=scores.get)
        return best_match, scores[best_match]

    def _calculate_weighted_score(self, content: str, indicators: Dict[str, List[str]]) -> float:
        total_score = 0.0
        for doc_type, patterns in indicators.items():
            total_score += self._detect_pattern_score(content, patterns)
        return total_score

    def _detect_pattern_score(self, content: str, patterns: List[str]) -> float:
        score = 0.0
        for pattern in patterns:
            if pattern.lower() in content.lower():
                score += 1.0
        return score / len(patterns) if patterns else 0.0

    def detect_segmentation_strategy(self, content: str, doc_type: str) -> str:
        if doc_type == "academic":
            return "paragraphs"
        elif doc_type == "technical":
            return "sections"
        elif doc_type == "news":
            return "sentences"
        elif doc_type == "fiction":
            return "chapters"
        else:
            return "unknown"

    def _calculate_algorithm_density(self, content: str) -> float:
        algorithm_keywords = ["algorithm", "function", "procedure", "method"]
        return self._detect_pattern_score(content, algorithm_keywords)

    def _calculate_concept_complexity(self, content: str) -> float:
        complexity_keywords = ["complex", "advanced",
                               "sophisticated", "complicated"]
        return self._detect_pattern_score(content, complexity_keywords)

    def _calculate_implementation_detail_level(self, content: str) -> float:
        detail_keywords = ["implementation", "code", "example", "sample"]
        return self._detect_pattern_score(content, detail_keywords)
