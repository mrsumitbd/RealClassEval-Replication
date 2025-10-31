
from typing import Tuple, Dict, List
import re


class DocumentAnalyzer:

    def analyze_document_type(self, content: str) -> Tuple[str, float]:
        indicators = {
            "technical": ["algorithm", "implementation", "complexity", "function", "method"],
            "narrative": ["story", "character", "plot", "setting", "theme"],
            "legal": ["clause", "agreement", "party", "law", "contract"]
        }

        scores = {}
        for doc_type, terms in indicators.items():
            scores[doc_type] = self._calculate_weighted_score(
                content, {doc_type: terms})

        max_type = max(scores, key=scores.get)
        return max_type, scores[max_type]

    def _calculate_weighted_score(self, content: str, indicators: Dict[str, List[str]]) -> float:
        total_score = 0.0
        for term_list in indicators.values():
            for term in term_list:
                total_score += content.lower().count(term.lower()) * (1.0 / len(term))
        return total_score

    def _detect_pattern_score(self, content: str, patterns: List[str]) -> float:
        score = 0.0
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            score += len(matches) * (1.0 / len(pattern))
        return score

    def detect_segmentation_strategy(self, content: str, doc_type: str) -> str:
        if doc_type == "technical":
            return "code_block"
        elif doc_type == "narrative":
            return "paragraph"
        elif doc_type == "legal":
            return "section"
        else:
            return "default"

    def _calculate_algorithm_density(self, content: str) -> float:
        algo_terms = ["algorithm", "complexity", "O(", "log n", "n^2"]
        return sum(content.lower().count(term.lower()) for term in algo_terms) / len(content.split())

    def _calculate_concept_complexity(self, content: str) -> float:
        complex_terms = ["recursion",
                         "dynamic programming", "graph", "tree", "hash"]
        return sum(content.lower().count(term.lower()) for term in complex_terms) / len(content.split())

    def _calculate_implementation_detail_level(self, content: str) -> float:
        detail_terms = ["function", "method",
                        "class", "interface", "implementation"]
        return sum(content.lower().count(term.lower()) for term in detail_terms) / len(content.split())
