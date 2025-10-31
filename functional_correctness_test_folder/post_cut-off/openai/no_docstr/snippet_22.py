
from typing import Tuple, Dict, List
import re
import math


class DocumentAnalyzer:
    # Keywords for different document types
    _type_indicators: Dict[str, List[str]] = {
        "technical": [
            "algorithm", "function", "class", "def", "return", "parameter",
            "input", "output", "complexity", "pseudo-code", "implementation",
            "data structure", "runtime", "memory", "performance"
        ],
        "legal": [
            "agreement", "party", "clause", "term", "condition", "obligation",
            "liability", "jurisdiction", "confidentiality", "warranty", "indemnity"
        ],
        "creative": [
            "story", "character", "plot", "setting", "dialogue", "theme",
            "narrative", "protagonist", "antagonist", "conflict", "resolution"
        ],
        "financial": [
            "balance sheet", "income statement", "cash flow", "assets",
            "liabilities", "equity", "revenue", "expense", "profit", "loss",
            "forecast", "valuation"
        ]
    }

    # Algorithmic terms for density calculation
    _algorithm_terms = {
        "if", "else", "for", "while", "do", "switch", "case", "break",
        "continue", "return", "function", "def", "class", "import",
        "from", "try", "except", "finally", "with", "as", "lambda",
        "yield", "pass", "raise", "assert", "global", "nonlocal",
        "del", "print", "input", "len", "range", "list", "dict",
        "set", "tuple", "str", "int", "float", "bool", "None"
    }

    # Patterns for segmentation strategy
    _segmentation_map = {
        "technical": "section",
        "legal": "paragraph",
        "creative": "paragraph",
        "financial": "section"
    }

    def analyze_document_type(self, content: str) -> Tuple[str, float]:
        """
        Determine the most likely document type and return it with a confidence score.
        """
        scores = {}
        for doc_type, indicators in self._type_indicators.items():
            scores[doc_type] = self._calculate_weighted_score(
                content, {doc_type: indicators})
        best_type = max(scores, key=scores.get)
        return best_type, scores[best_type]

    def _calculate_weighted_score(self, content: str, indicators: Dict[str, List[str]]) -> float:
        """
        Compute a weighted score for a single document type based on indicator patterns.
        """
        total_score = 0.0
        for doc_type, patterns in indicators.items():
            pattern_score = self._detect_pattern_score(content, patterns)
            # Weight by the number of patterns to give more importance to richer indicator sets
            weight = len(patterns)
            total_score += pattern_score * weight
        return total_score

    def _detect_pattern_score(self, content: str, patterns: List[str]) -> float:
        """
        Count occurrences of each pattern in the content and normalize by total patterns.
        """
        content_lower = content.lower()
        count = 0
        for pat in patterns:
            # Use word boundaries to avoid partial matches
            regex = r'\b' + re.escape(pat.lower()) + r'\b'
            matches = re.findall(regex, content_lower)
            count += len(matches)
        # Normalize by number of patterns to keep score between 0 and 1
        return count / len(patterns) if patterns else 0.0

    def detect_segmentation_strategy(self, content: str, doc_type: str) -> str:
        """
        Return the segmentation strategy based on document type.
        """
        return self._segmentation_map.get(doc_type, "paragraph")

    def _calculate_algorithm_density(self, content: str) -> float:
        """
        Ratio of algorithmic terms to total words.
        """
        words = re.findall(r'\b\w+\b', content.lower())
        if not words:
            return 0.0
        algo_count = sum(1 for w in words if w in self._algorithm_terms)
        return algo_count / len(words)

    def _calculate_concept_complexity(self, content: str) -> float:
        """
        Complexity based on average word length and vocabulary richness.
        """
        words = re.findall(r'\b\w+\b', content.lower())
        if not words:
            return 0.0
        avg_len = sum(len(w) for w in words) / len(words)
        unique_ratio = len(set(words)) / len(words)
        return avg_len * unique_ratio

    def _calculate_implementation_detail_level(self, content: str) -> float:
        """
        Ratio of code-like lines to total lines.
        """
        lines = content.splitlines()
        if not lines:
            return 0.0
        code_lines = 0
        for line in lines:
            stripped = line.strip()
            # Detect code fences or typical code patterns
            if stripped.startswith(("
