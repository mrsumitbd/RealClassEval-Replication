
import re
from typing import Dict, List, Tuple


class DocumentAnalyzer:
    """Enhanced document analyzer using semantic content analysis instead of mechanical structure detection"""

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def analyze_document_type(self, content: str) -> Tuple[str, float]:
        """
        Enhanced document type analysis based on semantic content patterns.

        Parameters
        ----------
        content : str
            Raw text of the document.

        Returns
        -------
        Tuple[str, float]
            (document_type, confidence_score)
        """
        # Define semantic indicators for each document type
        indicators: Dict[str, List[str]] = {
            "research_paper": [
                "abstract", "introduction", "related work", "methodology",
                "experiment", "results", "conclusion", "acknowledgement",
                "references", "theorem", "lemma", "proof",
            ],
            "blog_post": [
                "introduction", "summary", "takeaway", "personal", "opinion",
                "experience", "story", "tips", "tricks", "how-to",
            ],
            "technical_report": [
                "executive summary", "background", "scope", "method", "analysis",
                "findings", "recommendations", "appendix", "data set",
            ],
            "novel": [
                "chapter", "protagonist", "setting", "dialogue", "plot",
                "character", "conflict", "resolution", "theme",
            ],
            "manual": [
                "step", "procedure", "instruction", "setup", "configuration",
                "troubleshooting", "faq", "specification", "compatibility",
            ],
        }

        # Compute weighted scores for each type
        scores = {
            doc_type: self._calculate_weighted_score(
                content, {doc_type: indicators[doc_type]})
            for doc_type in indicators
        }

        # Determine best match
        best_type, best_score = max(scores.items(), key=lambda kv: kv[1])

        # Normalize confidence to [0, 1]
        max_score = max(scores.values())
        confidence = best_score / max_score if max_score > 0 else 0.0

        return best_type, confidence

    def detect_segmentation_strategy(self, content: str, doc_type: str) -> str:
        """
        Intelligently determine the best segmentation strategy based on content semantics
        rather than mechanical structure.

        Parameters
        ----------
        content : str
            Raw text of the document.
        doc_type : str
            Document type as returned by `analyze_document_type`.

        Returns
        -------
        str
            One of: "paragraph", "section", "algorithmic", "conceptual", "code_block".
        """
        # Compute densities
        algo_density = self._calculate_algorithm_density(content)
        concept_density = self._calculate_concept_complexity(content)
        impl_density = self._calculate_implementation_detail_level(content)

        # Heuristic rules
        if doc_type == "research_paper":
            if concept_density > 0.6:
                return "conceptual"
            if algo_density > 0.4:
                return "algorithmic"
            return "section"

        if doc_type == "technical_report":
            if impl_density > 0.5:
                return "code_block"
            return "section"

        if doc_type == "blog_post":
            return "paragraph"

        if doc_type == "novel":
            return "chapter"

        if doc_type == "manual":
            if impl_density > 0.4:
                return "code_block"
            return "section"

        # Default fallback
        return "paragraph"

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _calculate_weighted_score(self, content: str, indicators: Dict[str, List[str]]) -> float:
        """
        Calculate weighted semantic indicator scores.

        Parameters
        ----------
        content : str
            Document text.
        indicators : Dict[str, List[str]]
            Mapping from document type to list of indicator keywords.

        Returns
        -------
        float
            Normalized score in [0, 1].
        """
        content_lower = content.lower()
        total_words = len(re.findall(r"\b\w+\b", content_lower)) or 1

        # Count matches per indicator
        match_counts = {
            doc_type: sum(
                content_lower.count(keyword.lower()) for keyword in keywords
            )
            for doc_type, keywords in indicators.items()
        }

        # Weight by keyword frequency and normalize
        weighted = sum(match_counts.values())
        return weighted / total_words

    def _detect_pattern_score(self, content: str, patterns: List[str]) -> float:
        """
        Detect semantic pattern matching scores.

        Parameters
        ----------
        content : str
            Document text.
        patterns : List[str]
            List of regex patterns to search for.

        Returns
        -------
        float
            Score in [0, 1] based on pattern matches.
        """
        content_lower = content.lower()
        total_words = len(re.findall(r"\b\w+\b", content_lower)) or 1

        matches = 0
        for pat in patterns:
            matches += len(re.findall(pat, content_lower))

        return matches / total_words

    def _calculate_algorithm_density(self, content: str) -> float:
        """
        Calculate algorithm content density.

        Parameters
        ----------
        content : str
            Document text.

        Returns
        -------
        float
            Density in [0, 1].
        """
        algorithm_terms = [
            r"\balgorithm\b", r"\bprocedure\b", r"\bfunction\b", r"\bloop\b",
            r"\bfor\b", r"\bwhile\b", r"\bif\b", r"\belse\b", r"\bcase\b",
            r"\bswitch\b", r"\breturn\b", r"\bbreak\b", r"\bcontinue\b",
        ]
        return self._detect_pattern_score(content, algorithm_terms)

    def _calculate_concept_complexity(self, content: str) -> float:
        """
        Calculate concept complexity.

        Parameters
        ----------
        content : str
            Document text.

        Returns
        -------
        float
            Complexity in [0, 1].
        """
        concept_terms = [
            r"\btheorem\b", r"\blemma\b", r"\bproof\b", r"\bconjecture\b",
            r"\bhypothesis\b", r"\bdefinition\b", r"\bcorollary\b",
            r"\baxiom\b", r"\bpostulate\b", r"\bprinciple\b",
        ]
        return self._detect_pattern_score(content, concept_terms)

    def _calculate_implementation_detail_level(self, content: str) -> float:
        """
        Calculate implementation detail level.

        Parameters
        ----------
        content : str
            Document text.

        Returns
        -------
        float
            Detail level in [0, 1].
        """
        impl_terms = [
            r"\bclass\b", r"\bdef\b", r"\bint\b", r"\bfloat\b", r"\bstring\b",
            r"\bvariable\b", r"\bfunction\b", r"\bmethod\b", r"\bparameter\b",
            r"\bargument\b", r"\bmodule\b", r"\bimport\b", r"\bpackage\b",
            r"\blibrary\b", r"\bframework\b", r"\bAPI\b", r"\bendpoint\b",
        ]
        return self._detect_pattern_score(content, impl_terms)
