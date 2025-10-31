
from typing import Tuple, Dict, List
import re


class DocumentAnalyzer:

    def analyze_document_type(self, content: str) -> Tuple[str, float]:
        indicators = {
            "technical": ["algorithm", "implementation", "complexity", "optimization"],
            "narrative": ["story", "character", "plot", "setting"],
            "legal": ["clause", "jurisdiction", "agreement", "party"],
        }

        max_score = 0.0
        doc_type = "unknown"

        for dtype, terms in indicators.items():
            score = self._calculate_weighted_score(content, {dtype: terms})
            if score > max_score:
                max_score = score
                doc_type = dtype

        return (doc_type, max_score)

    def _calculate_weighted_score(self, content: str, indicators: Dict[str, List[str]]) -> float:
        score = 0.0
        for term in indicators.get(list(indicators.keys())[0], []):
            score += content.lower().count(term.lower()) * 0.1
        return score

    def _detect_pattern_score(self, content: str, patterns: List[str]) -> float:
        score = 0.0
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            score += len(matches) * 0.05
        return score

    def detect_segmentation_strategy(self, content: str, doc_type: str) -> str:
        if doc_type == "technical":
            return "section-based"
        elif doc_type == "narrative":
            return "paragraph-based"
        elif doc_type == "legal":
            return "clause-based"
        else:
            return "default"

    def _calculate_algorithm_density(self, content: str) -> float:
        algo_terms = ["algorithm", "sort", "search", "complexity"]
        count = sum(content.lower().count(term) for term in algo_terms)
        return count / len(content.split()) if len(content.split()) > 0 else 0.0

    def _calculate_concept_complexity(self, content: str) -> float:
        complex_terms = ["complexity", "abstract", "recursion", "polymorphism"]
        count = sum(content.lower().count(term) for term in complex_terms)
        return count / len(content.split()) if len(content.split()) > 0 else 0.0

    def _calculate_implementation_detail_level(self, content: str) -> float:
        detail_terms = ["implementation", "detail", "code", "function"]
        count = sum(content.lower().count(term) for term in detail_terms)
        return count / len(content.split()) if len(content.split()) > 0 else 0.0
