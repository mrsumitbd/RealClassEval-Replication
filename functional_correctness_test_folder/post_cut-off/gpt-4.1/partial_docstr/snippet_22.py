
import re
from typing import Tuple, Dict, List


class DocumentAnalyzer:

    def analyze_document_type(self, content: str) -> Tuple[str, float]:
        indicators = {
            "research": [
                "abstract", "introduction", "methodology", "experiment", "results", "conclusion", "references", "study", "analysis", "data"
            ],
            "manual": [
                "step", "procedure", "instruction", "how to", "guide", "usage", "install", "configuration", "setup", "troubleshoot"
            ],
            "report": [
                "summary", "findings", "recommendation", "background", "discussion", "objective", "scope", "conclusion", "appendix"
            ],
            "tutorial": [
                "example", "walkthrough", "lesson", "practice", "exercise", "demonstration", "learn", "follow these steps", "tip"
            ]
        }
        scores = {}
        for doc_type, words in indicators.items():
            scores[doc_type] = self._calculate_weighted_score(
                content, {doc_type: words})
        best_type = max(scores, key=scores.get)
        return best_type, scores[best_type]

    def _calculate_weighted_score(self, content: str, indicators: Dict[str, List[str]]) -> float:
        content_lower = content.lower()
        total_score = 0.0
        for doc_type, words in indicators.items():
            for word in words:
                pattern = r'\b' + re.escape(word.lower()) + r'\b'
                matches = re.findall(pattern, content_lower)
                total_score += len(matches)
        # Normalize by content length (in 1000s of chars)
        norm = max(1, len(content) // 1000)
        return total_score / norm

    def _detect_pattern_score(self, content: str, patterns: List[str]) -> float:
        content_lower = content.lower()
        score = 0
        for pattern in patterns:
            regex = re.compile(pattern, re.IGNORECASE)
            matches = regex.findall(content_lower)
            score += len(matches)
        # Normalize by number of patterns
        if patterns:
            return score / len(patterns)
        return 0.0

    def detect_segmentation_strategy(self, content: str, doc_type: str) -> str:
        headings = re.findall(
            r'^\s*(\d+\.\s+)?([A-Z][A-Za-z0-9 ]{2,})\s*$', content, re.MULTILINE)
        if doc_type == "research":
            if any("abstract" in h[1].lower() for h in headings) and any("references" in h[1].lower() for h in headings):
                return "sectioned (academic)"
            else:
                return "paragraphs"
        elif doc_type == "manual":
            if any("step" in h[1].lower() or "procedure" in h[1].lower() for h in headings):
                return "stepwise"
            else:
                return "bulleted"
        elif doc_type == "tutorial":
            if any("lesson" in h[1].lower() or "exercise" in h[1].lower() for h in headings):
                return "modular"
            else:
                return "linear"
        elif doc_type == "report":
            if any("summary" in h[1].lower() or "findings" in h[1].lower() for h in headings):
                return "sectioned (report)"
            else:
                return "paragraphs"
        else:
            return "unknown"

    def _calculate_algorithm_density(self, content: str) -> float:
        # Count code blocks or pseudocode patterns
        code_patterns = [
            r'
