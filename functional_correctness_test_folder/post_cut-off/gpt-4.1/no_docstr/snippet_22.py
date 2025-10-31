
import re
from typing import Tuple, Dict, List


class DocumentAnalyzer:

    def analyze_document_type(self, content: str) -> Tuple[str, float]:
        indicators = {
            "research": [
                "abstract", "introduction", "methodology", "results", "discussion", "conclusion", "references", "experiment", "study", "analysis"
            ],
            "tutorial": [
                "step by step", "how to", "example", "walkthrough", "guide", "instructions", "demonstration", "practice", "exercise"
            ],
            "manual": [
                "user guide", "manual", "instructions", "setup", "configuration", "troubleshooting", "installation", "requirements", "usage"
            ],
            "report": [
                "summary", "findings", "report", "data", "statistics", "overview", "conclusion", "recommendation"
            ]
        }
        scores = {}
        for doc_type, patterns in indicators.items():
            scores[doc_type] = self._calculate_weighted_score(
                content, {doc_type: patterns})
        best_type = max(scores, key=scores.get)
        return best_type, scores[best_type]

    def _calculate_weighted_score(self, content: str, indicators: Dict[str, List[str]]) -> float:
        content_lower = content.lower()
        total_score = 0.0
        for doc_type, patterns in indicators.items():
            score = self._detect_pattern_score(content_lower, patterns)
            total_score += score
        return total_score

    def _detect_pattern_score(self, content: str, patterns: List[str]) -> float:
        score = 0.0
        for pattern in patterns:
            occurrences = len(re.findall(
                r'\b' + re.escape(pattern.lower()) + r'\b', content.lower()))
            score += occurrences
        if len(patterns) > 0:
            score = score / len(patterns)
        return score

    def detect_segmentation_strategy(self, content: str, doc_type: str) -> str:
        content_lower = content.lower()
        if doc_type == "tutorial":
            if re.search(r'\b(step|exercise|practice|walkthrough)\b', content_lower):
                return "stepwise"
            elif re.search(r'\b(section|part|chapter)\b', content_lower):
                return "sectional"
            else:
                return "linear"
        elif doc_type == "research":
            if re.search(r'\b(abstract|introduction|methodology|results|discussion|conclusion)\b', content_lower):
                return "academic"
            else:
                return "sectional"
        elif doc_type == "manual":
            if re.search(r'\b(troubleshooting|setup|installation|configuration)\b', content_lower):
                return "task-based"
            else:
                return "sectional"
        elif doc_type == "report":
            if re.search(r'\b(summary|findings|recommendation|overview)\b', content_lower):
                return "summary-based"
            else:
                return "sectional"
        else:
            return "unknown"

    def _calculate_algorithm_density(self, content: str) -> float:
        code_keywords = [
            "algorithm", "procedure", "function", "method", "pseudo-code", "pseudocode", "step", "input", "output", "return", "if", "else", "for", "while"
        ]
        code_blocks = len(re.findall(r'
