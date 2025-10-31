import re
import math
from typing import Dict, List, Tuple


class DocumentAnalyzer:
    '''Enhanced document analyzer using semantic content analysis instead of mechanical structure detection'''

    def analyze_document_type(self, content: str) -> Tuple[str, float]:
        '''
        Enhanced document type analysis based on semantic content patterns
        Returns:
            Tuple[str, float]: (document_type, confidence_score)
        '''
        if not content or not isinstance(content, str):
            return ("unknown", 0.0)

        text = content.lower()
        # Truncate extremely long inputs for performance while keeping enough signal
        if len(text) > 500_000:
            text = text[:500_000]

        doc_indicators: Dict[str, Dict[str, List[str]]] = {
            "research_paper": {
                "strong": [
                    "abstract", "introduction", "related work", "method", "methods",
                    "experiments", "results", "conclusion", "references", "appendix",
                    "we propose", "in this paper", "et al."
                ],
                "medium": [
                    "state-of-the-art", "baseline", "significant improvement",
                    "dataset", "evaluation", "statistically significant"
                ],
                "weak": ["figure", "table", "supplementary"]
            },
            "tutorial": {
                "strong": [
                    "step-by-step", "follow along", "let's build", "let’s build",
                    "tutorial", "walkthrough", "prerequisites"
                ],
                "medium": ["first,", "next,", "finally,", "in this tutorial", "guide", "hands-on"],
                "weak": ["tip:", "note:", "pro tip"]
            },
            "api_reference": {
                "strong": [
                    "endpoint", "request", "response", "parameters", "returns",
                    "status code", "http", "curl", "authentication", "header",
                    "query string", "json schema"
                ],
                "medium": [":param", "args", "kwargs", "schema", "example request", "response body"],
                "weak": ["rate limit", "error code"],
            },
            "code_documentation": {
                "strong": [
                    "class ", "def ", "public ", "private ", "interface ",
                    "@param", ":param", "args:", "returns:", "throws", "example:",
                    "usage:", "parameters:", "attributes:"
                ],
                "medium": ["module", "package", "import ", "namespace", "constructor", "method"],
                "weak": ["deprecated", "see also", "overrides"]
            },
            "product_manual": {
                "strong": [
                    "safety", "warning", "installation", "maintenance",
                    "troubleshooting", "specifications", "setup", "operation"
                ],
                "medium": ["warranty", "compliance", "instructions", "operating", "features"],
                "weak": ["package contents", "contact support"]
            },
            "legal_document": {
                "strong": [
                    "hereby", "whereas", "thereof", "herein", "party", "agreement",
                    "governing law", "witnesseth", "term and termination"
                ],
                "medium": ["indemnify", "severability", "liability", "arbitration", "jurisdiction", "assignment"],
                "weak": ["counterparts", "force majeure"]
            },
            "news_article": {
                "strong": [
                    "according to", "spokesperson", "breaking", "officials",
                    "on monday", "on tuesday", "on wednesday", "on thursday",
                    "on friday", "on saturday", "on sunday", "said", "reporter"
                ],
                "medium": ["headline", "update", "press", "editor", "source said", "investigation"],
                "weak": ["photo", "reuters", "associated press", "ap"]
            },
            "faq": {
                "strong": ["faq", "frequently asked questions", "q:", "a:"],
                "medium": ["question", "answer", "how do i", "what is", "common questions"],
                "weak": ["troubleshoot", "common issues"]
            },
            "blog_post": {
                "strong": ["i think", "in my opinion", "today i", "story", "my experience"],
                "medium": ["comment", "subscribe", "share", "update", "thanks for reading"],
                "weak": ["posted on", "comments", "newsletter"]
            },
            "dataset_card": {
                "strong": ["dataset", "samples", "license", "citation", "splits", "features", "download", "version"],
                "medium": ["benchmark", "preprocessing", "train", "test", "validation", "metrics"],
                "weak": ["tfds", "huggingface", "metadata", "config"]
            }
        }

        scores: Dict[str, float] = {}
        for dtype, indicators in doc_indicators.items():
            scores[dtype] = self._calculate_weighted_score(text, indicators)

        # Unknown if all scores are very low
        best_type = max(scores, key=scores.get)
        top_score = scores[best_type]
        second_score = max([v for k, v in scores.items()
                           if k != best_type] or [0.0])

        if top_score < 0.15:
            return ("unknown", round(top_score, 3))

        # Confidence based on margin between top two and absolute magnitude
        margin = max(0.0, top_score - second_score)
        confidence = min(1.0, 0.5 * top_score + 0.5 *
                         (margin / (top_score + 1e-6)))
        return (best_type, round(confidence, 3))

    def _calculate_weighted_score(self, content: str, indicators: Dict[str, List[str]]) -> float:
        '''Calculate weighted semantic indicator scores'''
        weight_map: Dict[str, float] = {
            "strong": 1.0,
            "medium": 0.6,
            "weak": 0.3,
            "negative": -0.8,
        }
        total = 0.0
        pos_cap = 0.0
        neg_cap = 0.0

        for key, patterns in indicators.items():
            weight = weight_map.get(key, 0.5)
            score = self._detect_pattern_score(content, patterns)
            total += weight * score
            if weight > 0:
                pos_cap += weight
            elif weight < 0:
                neg_cap += -weight

        denom = pos_cap + neg_cap + 1e-6
        normalized = (total + neg_cap) / denom if denom > 0 else 0.0
        return max(0.0, min(1.0, normalized))

    def _detect_pattern_score(self, content: str, patterns: List[str]) -> float:
        '''Detect semantic pattern matching scores'''
        if not patterns:
            return 0.0
        text = content.lower()
        words = max(1, len(re.findall(r'\w+', text)))
        count = 0

        for p in patterns:
            p_lower = p.lower()
            # Use word boundary for alphanumeric patterns; else literal search
            if re.search(r'[A-Za-z0-9]', p_lower):
                regex = re.compile(
                    r'\b' + re.escape(p_lower) + r'\b', flags=re.IGNORECASE)
            else:
                regex = re.compile(re.escape(p_lower), flags=re.IGNORECASE)
            matches = regex.findall(text)
            count += len(matches)

        # Normalize by content length (per 1000 words) and squash
        density = count / (words / 1000.0)
        score = 1.0 - math.exp(-0.4 * density)
        return max(0.0, min(1.0, score))

    def detect_segmentation_strategy(self, content: str, doc_type: str) -> str:
        '''
        Intelligently determine the best segmentation strategy based on content semantics rather than mechanical structure
        '''
        if not content:
            return "paragraphs"

        text = content
        lower = text.lower()
        lines = [ln for ln in text.splitlines()]
        total_lines = max(1, len(lines))

        # Quick structural signals (still semantically motivated)
        has_code_fence = ("```" in text) or ("~~~" in text)
        bullet_lines = sum(1 for ln in lines if re.match(
            r'^\s*(?:[-*•]+|\d+\.)\s+', ln))
        bullet_ratio = bullet_lines / total_lines

        heading_lines = sum(
            1 for ln in lines if re.match(r'^\s*#{1,6}\s+\S', ln))
        underline_headings = sum(1 for i in range(len(lines) - 1)
                                 if re.match(r'^\S', lines[i]) and re.match(r'^\s*(?:=+|-+)\s*$', lines[i + 1]))
        named_sections = sum(1 for ln in lines if re.match(
            r'^\s*(abstract|introduction|methods?|results?|discussion|conclusion|appendix|references|table of contents)\b',
            ln.strip().lower()))
        heading_signal = (heading_lines + underline_headings +
                          named_sections) / total_lines

        algo_density = self._calculate_algorithm_density(text)
        concept_complexity = self._calculate_concept_complexity(text)
        impl_detail = self._calculate_implementation_detail_level(text)

        # Special-case detection for QA-style docs
        qa_lines = sum(1 for ln in lines if re.match(
            r'^\s*(q[:\-]?|question[:\-]?|a[:\-]?|answer[:\-]?)\s*', ln.lower()))
        qa_ratio = qa_lines / total_lines

        if doc_type == "faq" or qa_ratio > 0.08:
            return "qa_pairs"

        if bullet_ratio > 0.25 and impl_detail < 0.4:
            return "bullets"

        if doc_type in ("api_reference", "code_documentation"):
            if has_code_fence or impl_detail > 0.6:
                if heading_signal > 0.06:
                    return "sections"
                return "code_blocks"
            return "sections" if heading_signal > 0.05 else "paragraphs"

        if doc_type == "research_paper":
            if heading_signal > 0.04 or concept_complexity > 0.5:
                return "sections"
            return "paragraphs"

        if doc_type == "legal_document":
            return "sections" if heading_signal > 0.03 else "paragraphs"

        if doc_type == "product_manual":
            if bullet_ratio > 0.18:
                return "bullets"
            return "sections" if heading_signal > 0.04 else "paragraphs"

        if doc_type == "tutorial":
            if has_code_fence and impl_detail > 0.5:
                return "code_blocks"
            if bullet_ratio > 0.18:
                return "bullets"
            return "sections" if heading_signal > 0.04 else "paragraphs"

        if doc_type in ("news_article", "blog_post"):
            # Prefer paragraphs for narrative content
            return "paragraphs"

        if doc_type == "dataset_card":
            if heading_signal > 0.05:
                return "sections"
            if bullet_ratio > 0.2:
                return "bullets"
            return "paragraphs"

        # Fallback based on semantic metrics
        if has_code_fence or algo_density > 0.45:
            return "code_blocks"
        if heading_signal > 0.05:
            return "sections"
        if bullet_ratio > 0.2:
            return "bullets"
        return "paragraphs"

    def _calculate_algorithm_density(self, content: str) -> float:
        '''Calculate algorithm content density'''
        text = content.lower()
        alg_patterns = [
            "algorithm", "procedure", "pseudocode", "pseudo-code", "complexity",
            "o(", "o(n", "o(n^", "o(m", "o(k", "o(log", "omega(", "theta(",
            "theorem", "lemma", "proof", "corollary", "assumption", "proposition",
            "for each", "while", "if", "return", "step", "invariant", "runtime"
        ]
        # Count code-like constructs
        code_like_lines = sum(1 for ln in content.splitlines() if re.match(
            r'^\s*(def |class |@|public |private |function |var |let |const |#include|template|using )', ln))
        code_fences = 1 if ("```" in content or "~~~" in content) else 0

        base_score = self._detect_pattern_score(text, alg_patterns)
        length_factor = min(1.0, len(content) / 20000.0)
        code_signal = 1.0 - \
            math.exp(-0.4 * (code_like_lines + 4 * code_fences))

        combined = 0.55 * base_score + 0.35 * code_signal + 0.10 * length_factor
        return max(0.0, min(1.0, combined))

    def _calculate_concept_complexity(self, content: str) -> float:
        '''Calculate concept complexity'''
        text = content
        lower = text.lower()
        words = re.findall(r"[A-Za-z']+", text)
        word_count = max(1, len(words))
        sentences = re.split(r'[.!?]+', text)
        sent_count = max(1, len([s for s in sentences if s.strip()]))

        avg_sent_len = word_count / sent_count
        avg_len_norm = min(1.0, avg_sent_len / 30.0)

        long_words = sum(1 for w in words if len(w) >= 12)
        long_ratio = long_words / word_count

        academic_terms = [
            "we propose", "novel", "baseline", "dataset", "architecture",
            "optimization", "derivation", "formulation", "statistically significant",
            "hypothesis", "contribution", "empirical", "theoretical", "generalization"
        ]
        term_score = self._detect_pattern_score(lower, academic_terms)

        complexity = 0.45 * avg_len_norm + 0.25 * \
            min(1.0, 3.0 * long_ratio) + 0.30 * term_score
        return max(0.0, min(1.0, complexity))

    def _calculate_implementation_detail_level(self, content: str) -> float:
        '''Calculate implementation detail level'''
        lines = content.splitlines()
        total_lines = max(1, len(lines))
        lower = content.lower()

        impl_markers = [
            "parameters:", "args:", "arguments:", "returns:", "raises:", "throws",
            "example:", "examples:", "usage:", ":param", "@param", "@return",
            "response:", "request:", "endpoint", "http", "curl", "status code",
            "schema", "field", "type:", "default:"
        ]
        marker_score = self._detect_pattern_score(lower, impl_markers)

        code_like = sum(1 for ln in lines if re.match(
            r'^\s*(def |class |@|public |private |protected |function |var |let |const |#include|template|using )', ln))
        code_fence = 1 if ("```" in content or "~~~" in content) else 0
        code_signal = 1.0 - math.exp(-0.35 * (code_like + 5 * code_fence))

        signatures = len(re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\s*\(', content))
        signature_density = signatures / max(1.0, total_lines)
        signature_score = 1.0 - math.exp(-4.0 * signature_density)

        detail = 0.45 * marker_score + 0.35 * code_signal + 0.20 * signature_score
        return max(0.0, min(1.0, detail))
