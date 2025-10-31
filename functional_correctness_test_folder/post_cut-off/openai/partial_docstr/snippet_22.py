
from typing import Tuple, Dict, List
import re
import math
import collections


class DocumentAnalyzer:
    # Simple indicator sets for different document types
    _type_indicators: Dict[str, Dict[str, List[str]]] = {
        "scientific": {
            "keywords": ["abstract", "introduction", "methods", "results", "conclusion"],
            "patterns": [r"\b[0-9]+\b", r"\b[0-9]+\.[0-9]+\b"]
        },
        "book": {
            "keywords": ["chapter", "section", "prologue", "epilogue"],
            "patterns": [r"\bChapter\s+[0-9]+\b", r"\bSection\s+[0-9]+\b"]
        },
        "article": {
            "keywords": ["byline", "author", "date", "summary"],
            "patterns": [r"\b[0-9]{4}\b"]
        }
    }

    # Weighted scores for semantic indicators
    _indicator_weights: Dict[str, float] = {
        "keywords": 0.6,
        "patterns": 0.4
    }

    def analyze_document_type(self, content: str) -> Tuple[str, float]:
        """Detect document type and return confidence score."""
        scores: Dict[str, float] = {}
        for doc_type, indicators in self._type_indicators.items():
            score = self._calculate_weighted_score(content, indicators)
            scores[doc_type] = score
        # Choose type with highest score
        best_type = max(scores, key=scores.get)
        confidence = scores[best_type] / \
            sum(scores.values()) if scores else 0.0
        return best_type, confidence

    def _calculate_weighted_score(self, content: str, indicators: Dict[str, List[str]]) -> float:
        """Calculate weighted semantic indicator scores."""
        total = 0.0
        for key, weight in self._indicator_weights.items():
            if key == "keywords":
                total += weight * \
                    self._detect_pattern_score(
                        content, indicators.get(key, []))
            elif key == "patterns":
                total += weight * \
                    self._detect_pattern_score(
                        content, indicators.get(key, []))
        return total

    def _detect_pattern_score(self, content: str, patterns: List[str]) -> float:
        """Return a score based on how many patterns match."""
        if not patterns:
            return 0.0
        matches = sum(1 for pat in patterns if re.search(
            pat, content, re.IGNORECASE))
        return matches / len(patterns)

    def detect_segmentation_strategy(self, content: str, doc_type: str) -> str:
        """Return segmentation strategy based on document type."""
        if doc_type == "scientific":
            return "section"
        if doc_type == "book":
            return "chapter"
        return "paragraph"

    def _calculate_algorithm_density(self, content: str) -> float:
        """Calculate density of algorithmic constructs."""
        tokens = re.findall(
            r"\b(?:for|while|if|else|elif|switch|case|function|def|class|return)\b", content, re.IGNORECASE)
        return len(tokens) / max(1, len(content.split()))

    def _calculate_concept_complexity(self, content: str) -> float:
        """Calculate concept complexity based on unique word count."""
        words = re.findall(r"\b\w+\b", content.lower())
        unique = set(words)
        return len(unique) / max(1, len(words))

    def _calculate_implementation_detail_level(self, content: str) -> float:
        """Calculate level of implementation detail."""
        code_tokens = re.findall(
            r"\b(?:def|class|import|from|return|print|if|else|elif|for|while|try|except)\b", content, re.IGNORECASE)
        return len(code_tokens) / max(1, len(content.split()))
