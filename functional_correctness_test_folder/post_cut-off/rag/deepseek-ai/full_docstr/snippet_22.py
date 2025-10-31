
from typing import Dict, List, Tuple
import re


class DocumentAnalyzer:
    '''Enhanced document analyzer using semantic content analysis instead of mechanical structure detection'''

    def analyze_document_type(self, content: str) -> Tuple[str, float]:
        '''
        Enhanced document type analysis based on semantic content patterns
        Returns:
            Tuple[str, float]: (document_type, confidence_score)
        '''
        document_indicators = {
            "technical": ["algorithm", "implementation", "complexity", "optimization"],
            "legal": ["clause", "jurisdiction", "hereby", "notwithstanding"],
            "business": ["strategy", "market", "revenue", "stakeholder"],
            "scientific": ["hypothesis", "methodology", "results", "conclusion"]
        }

        scores = {}
        for doc_type, indicators in document_indicators.items():
            scores[doc_type] = self._calculate_weighted_score(
                content, {doc_type: indicators})

        max_score = max(scores.values())
        best_type = max(scores, key=scores.get)
        confidence = max_score / \
            sum(scores.values()) if sum(scores.values()) > 0 else 0.0

        return (best_type, confidence)

    def _calculate_weighted_score(self, content: str, indicators: Dict[str, List[str]]) -> float:
        '''Calculate weighted semantic indicator scores'''
        total_score = 0.0
        for indicator_list in indicators.values():
            for indicator in indicator_list:
                total_score += self._detect_pattern_score(content, [indicator])
        return total_score

    def _detect_pattern_score(self, content: str, patterns: List[str]) -> float:
        '''Detect semantic pattern matching scores'''
        score = 0.0
        content_lower = content.lower()
        for pattern in patterns:
            matches = re.findall(
                r'\b' + re.escape(pattern.lower()) + r'\b', content_lower)
            score += len(matches)
        return score

    def detect_segmentation_strategy(self, content: str, doc_type: str) -> str:
        '''
        Intelligently determine the best segmentation strategy based on content semantics rather than mechanical structure
        '''
        if doc_type == "technical":
            algo_density = self._calculate_algorithm_density(content)
            if algo_density > 0.5:
                return "algorithmic_blocks"
            else:
                return "conceptual_sections"
        elif doc_type == "legal":
            return "clause_hierarchy"
        elif doc_type == "business":
            return "topic_sections"
        elif doc_type == "scientific":
            return "imrad_structure"
        else:
            return "generic_sections"

    def _calculate_algorithm_density(self, content: str) -> float:
        '''Calculate algorithm content density'''
        algo_keywords = ["algorithm", "pseudocode",
                         "complexity", "O(", "Θ(", "Ω("]
        total_keywords = sum(self._detect_pattern_score(
            content, [kw]) for kw in algo_keywords)
        word_count = len(content.split())
        return total_keywords / word_count if word_count > 0 else 0.0

    def _calculate_concept_complexity(self, content: str) -> float:
        '''Calculate concept complexity'''
        complex_terms = ["recursion", "polynomial",
                         "nondeterministic", "heuristic"]
        total_terms = sum(self._detect_pattern_score(
            content, [term]) for term in complex_terms)
        word_count = len(content.split())
        return total_terms / word_count if word_count > 0 else 0.0

    def _calculate_implementation_detail_level(self, content: str) -> float:
        '''Calculate implementation detail level'''
        detail_keywords = ["function", "method",
                           "class", "interface", "parameter"]
        total_keywords = sum(self._detect_pattern_score(
            content, [kw]) for kw in detail_keywords)
        word_count = len(content.split())
        return total_keywords / word_count if word_count > 0 else 0.0
