
from typing import Tuple, Dict, List
import re
from collections import defaultdict


class DocumentAnalyzer:
    '''Enhanced document analyzer using semantic content analysis instead of mechanical structure detection'''

    def analyze_document_type(self, content: str) -> Tuple[str, float]:
        '''
        Enhanced document type analysis based on semantic content patterns
        Returns:
            Tuple[str, float]: (document_type, confidence_score)
        '''
        indicators = {
            "technical": ["algorithm", "implementation", "complexity", "optimization", "runtime"],
            "legal": ["clause", "jurisdiction", "hereinafter", "party", "agreement"],
            "business": ["strategy", "market", "revenue", "growth", "investment"],
            "scientific": ["hypothesis", "experiment", "results", "methodology", "conclusion"]
        }

        scores = {}
        for doc_type, terms in indicators.items():
            scores[doc_type] = self._calculate_weighted_score(
                content, {doc_type: terms})

        max_score = max(scores.values())
        best_type = max(scores, key=scores.get)
        confidence = max_score / \
            sum(scores.values()) if sum(scores.values()) > 0 else 0.0

        return (best_type, confidence)

    def _calculate_weighted_score(self, content: str, indicators: Dict[str, List[str]]) -> float:
        '''Calculate weighted semantic indicator scores'''
        score = 0.0
        for term in indicators.get(list(indicators.keys())[0], []):
            score += self._detect_pattern_score(content, [term])
        return score

    def _detect_pattern_score(self, content: str, patterns: List[str]) -> float:
        '''Detect semantic pattern matching scores'''
        score = 0.0
        content_lower = content.lower()
        for pattern in patterns:
            score += len(re.findall(r'\b' +
                         re.escape(pattern.lower()) + r'\b', content_lower))
        return score

    def detect_segmentation_strategy(self, content: str, doc_type: str) -> str:
        '''
        Intelligently determine the best segmentation strategy based on content semantics rather than mechanical structure
        '''
        strategies = {
            "technical": "algorithmic_steps",
            "legal": "clause_based",
            "business": "section_based",
            "scientific": "methodology_based"
        }
        return strategies.get(doc_type, "default_section_based")

    def _calculate_algorithm_density(self, content: str) -> float:
        '''Calculate algorithm content density'''
        algorithm_terms = ["algorithm", "pseudocode",
                           "complexity", "O(", "Ω(", "Θ("]
        total_terms = len(content.split())
        if total_terms == 0:
            return 0.0
        algorithm_terms_count = self._detect_pattern_score(
            content, algorithm_terms)
        return algorithm_terms_count / total_terms

    def _calculate_concept_complexity(self, content: str) -> float:
        '''Calculate concept complexity'''
        complex_terms = ["complexity", "optimization",
                         "nondeterministic", "heuristic", "recursive"]
        total_terms = len(content.split())
        if total_terms == 0:
            return 0.0
        complex_terms_count = self._detect_pattern_score(
            content, complex_terms)
        return complex_terms_count / total_terms

    def _calculate_implementation_detail_level(self, content: str) -> float:
        '''Calculate implementation detail level'''
        detail_terms = ["implementation", "code",
                        "function", "class", "method", "variable"]
        total_terms = len(content.split())
        if total_terms == 0:
            return 0.0
        detail_terms_count = self._detect_pattern_score(content, detail_terms)
        return detail_terms_count / total_terms
