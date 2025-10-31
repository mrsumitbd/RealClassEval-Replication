
import re
from typing import Tuple, Dict, List


class DocumentAnalyzer:
    '''Enhanced document analyzer using semantic content analysis instead of mechanical structure detection'''

    # Semantic indicators for different document types
    _SEMANTIC_INDICATORS = {
        "research_paper": [
            "abstract", "introduction", "methodology", "results", "discussion", "conclusion", "references",
            "experiment", "dataset", "analysis", "statistical", "significant", "hypothesis", "literature review"
        ],
        "technical_report": [
            "overview", "system architecture", "implementation", "evaluation", "performance", "specification",
            "design", "requirements", "testing", "deployment", "configuration", "benchmark"
        ],
        "tutorial": [
            "step by step", "how to", "walkthrough", "example", "guide", "instructions", "tips", "tricks",
            "demonstration", "practice", "exercise", "lesson", "introduction", "summary"
        ],
        "manual": [
            "user guide", "manual", "instructions", "operation", "setup", "installation", "troubleshooting",
            "maintenance", "configuration", "safety", "warranty", "specifications"
        ],
        "proposal": [
            "proposal", "objective", "scope", "budget", "timeline", "deliverables", "stakeholder", "plan",
            "expected outcome", "justification", "background", "resources"
        ]
    }

    # Patterns for segmentation strategies
    _SEGMENTATION_PATTERNS = {
        "section_based": [
            "introduction", "background", "methodology", "results", "discussion", "conclusion", "references",
            "overview", "system architecture", "implementation", "evaluation"
        ],
        "step_based": [
            "step", "step by step", "first", "next", "then", "finally", "example", "exercise", "practice"
        ],
        "topic_based": [
            "topic", "concept", "idea", "theme", "subject", "lesson", "module"
        ],
        "procedure_based": [
            "procedure", "process", "workflow", "operation", "instructions", "setup", "installation"
        ]
    }

    def analyze_document_type(self, content: str) -> Tuple[str, float]:
        '''
        Enhanced document type analysis based on semantic content patterns
        Returns:
            Tuple[str, float]: (document_type, confidence_score)
        '''
        scores = {}
        for doc_type, indicators in self._SEMANTIC_INDICATORS.items():
            score = self._calculate_weighted_score(
                content, {doc_type: indicators})
            scores[doc_type] = score
        best_type = max(scores, key=scores.get)
        confidence = scores[best_type]
        # Normalize confidence to [0, 1]
        max_possible = max(scores.values()) if scores else 1.0
        confidence = confidence / max_possible if max_possible > 0 else 0.0
        return best_type, round(confidence, 3)

    def _calculate_weighted_score(self, content: str, indicators: Dict[str, List[str]]) -> float:
        '''Calculate weighted semantic indicator scores'''
        content_lower = content.lower()
        total_score = 0.0
        for doc_type, patterns in indicators.items():
            pattern_score = self._detect_pattern_score(content_lower, patterns)
            # Weight: more patterns matched, higher score
            total_score += pattern_score * len(patterns)
        return total_score

    def _detect_pattern_score(self, content: str, patterns: List[str]) -> float:
        '''Detect semantic pattern matching scores'''
        score = 0.0
        for pattern in patterns:
            # Use word boundaries for single words, substring for phrases
            if " " in pattern:
                matches = len(re.findall(
                    re.escape(pattern), content, re.IGNORECASE))
            else:
                matches = len(re.findall(
                    r'\b' + re.escape(pattern) + r'\b', content, re.IGNORECASE))
            score += matches
        # Normalize by number of patterns
        if patterns:
            score = score / len(patterns)
        return score

    def detect_segmentation_strategy(self, content: str, doc_type: str) -> str:
        '''
        Intelligently determine the best segmentation strategy based on content semantics rather than mechanical structure
        '''
        content_lower = content.lower()
        strategy_scores = {}
        for strategy, patterns in self._SEGMENTATION_PATTERNS.items():
            score = self._detect_pattern_score(content_lower, patterns)
            strategy_scores[strategy] = score
        # Heuristic: for tutorials, prefer step_based; for research/technical, prefer section_based
        if doc_type in ("tutorial",) and strategy_scores["step_based"] > 0.2:
            return "step_based"
        if doc_type in ("research_paper", "technical_report") and strategy_scores["section_based"] > 0.2:
            return "section_based"
        # Otherwise, pick the highest scoring strategy
        best_strategy = max(strategy_scores, key=strategy_scores.get)
        return best_strategy

    def _calculate_algorithm_density(self, content: str) -> float:
        '''Calculate algorithm content density'''
        # Look for algorithmic keywords and code-like patterns
        algorithm_keywords = [
            "algorithm", "procedure", "pseudo-code", "pseudocode", "step", "input", "output", "initialize",
            "repeat", "while", "for each", "if", "else", "return", "function", "procedure", "complexity"
        ]
        code_patterns = [
            r"\bdef\b", r"\bclass\b", r"\bfor\b", r"\bwhile\b", r"\bif\b", r"\breturn\b", r"\bimport\b"
        ]
        text = content.lower()
        keyword_count = sum(len(re.findall(
            r'\b' + re.escape(word) + r'\b', text)) for word in algorithm_keywords)
        code_count = sum(len(re.findall(pattern, text))
                         for pattern in code_patterns)
        total_words = len(re.findall(r'\w+', text))
        density = (keyword_count + code_count) / \
            total_words if total_words > 0 else 0.0
        return round(density, 3)

    def _calculate_concept_complexity(self, content: str) -> float:
        '''Calculate concept complexity'''
        # Estimate by average sentence length and unique technical terms
        sentences = re.split(r'[.!?]', content)
        sentences = [s.strip() for s in sentences if s.strip()]
        if not sentences:
            return 0.0
        words = re.findall(r'\w+', content)
        avg_sentence_length = len(words) / len(sentences) if sentences else 0
        # Technical terms: words longer than 8 chars or containing digits/symbols
        technical_terms = set(w for w in words if len(w)
                              > 8 or re.search(r'\d|_', w))
        complexity = (avg_sentence_length *
                      len(technical_terms)) / (len(words) + 1)
        return round(complexity, 3)

    def _calculate_implementation_detail_level(self, content: str) -> float:
        '''Calculate implementation detail level'''
        # Look for implementation-specific words and code snippets
        detail_keywords = [
            "implementation", "code", "snippet", "example", "source code", "function", "class", "variable",
            "parameter", "argument", "return", "output", "input", "initialize", "setup", "configuration"
        ]
        code_snippet_pattern = r"
