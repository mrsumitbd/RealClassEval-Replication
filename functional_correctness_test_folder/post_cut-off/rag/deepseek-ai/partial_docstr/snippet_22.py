
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
        indicators = {
            "technical": ["algorithm", "implementation", "complexity", "optimization"],
            "legal": ["clause", "jurisdiction", "hereby", "notwithstanding"],
            "business": ["strategy", "market", "revenue", "stakeholder"],
        }

        scores = {}
        for doc_type, patterns in indicators.items():
            scores[doc_type] = self._calculate_weighted_score(
                content, {doc_type: patterns})

        best_type = max(scores.items(), key=lambda x: x[1])
        return best_type

    def _calculate_weighted_score(self, content: str, indicators: Dict[str, List[str]]) -> float:
        '''Calculate weighted semantic indicator scores'''
        total_score = 0.0
        for doc_type, patterns in indicators.items():
            total_score += self._detect_pattern_score(content, patterns)
        return total_score / len(indicators) if indicators else 0.0

    def _detect_pattern_score(self, content: str, patterns: List[str]) -> float:
        '''Detect semantic pattern matching scores'''
        score = 0.0
        content_lower = content.lower()
        for pattern in patterns:
            matches = re.findall(
                r'\b' + re.escape(pattern.lower()) + r'\b', content_lower)
            score += len(matches) * 0.1  # Weight per match
        return min(score, 1.0)  # Cap at 1.0

    def detect_segmentation_strategy(self, content: str, doc_type: str) -> str:
        '''
        Intelligently determine the best segmentation strategy based on content semantics rather than mechanical structure
        '''
        if doc_type == "technical":
            algo_density = self._calculate_algorithm_density(content)
            concept_complexity = self._calculate_concept_complexity(content)
            if algo_density > 0.5 and concept_complexity > 0.5:
                return "algorithmic_breakdown"
            else:
                return "sectional"
        elif doc_type == "legal":
            return "clause_based"
        elif doc_type == "business":
            return "topic_based"
        else:
            return "default"

    def _calculate_algorithm_density(self, content: str) -> float:
        '''Calculate algorithm content density'''
        algo_keywords = ["algorithm", "complexity",
                         "O(", "runtime", "optimize"]
        matches = sum(len(re.findall(r'\b' + re.escape(kw.lower()) +
                      r'\b', content.lower())) for kw in algo_keywords)
        total_words = len(content.split())
        return matches / total_words if total_words > 0 else 0.0

    def _calculate_concept_complexity(self, content: str) -> float:
        '''Calculate concept complexity'''
        complex_keywords = ["recursion",
                            "dynamic programming", "graph", "tree", "NP-hard"]
        matches = sum(len(re.findall(r'\b' + re.escape(kw.lower()) +
                      r'\b', content.lower())) for kw in complex_keywords)
        total_words = len(content.split())
        return matches / total_words if total_words > 0 else 0.0

    def _calculate_implementation_detail_level(self, content: str) -> float:
        '''Calculate implementation detail level'''
        detail_keywords = ["function", "method",
                           "class", "interface", "implementation"]
        matches = sum(len(re.findall(r'\b' + re.escape(kw.lower()) +
                      r'\b', content.lower())) for kw in detail_keywords)
        total_words = len(content.split())
        return matches / total_words if total_words > 0 else 0.0
