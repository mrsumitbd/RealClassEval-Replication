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
        text = (content or "").strip()
        if not text:
            return ("unknown", 0.0)

        lc = text.lower()

        doc_indicators: Dict[str, Dict[str, List[str]]] = {
            "research_paper": {
                "core": [
                    "abstract", "introduction", "related work", "method", "methods",
                    "experiments", "results", "conclusion", "references", "dataset",
                    "evaluation", "discussion"
                ],
                "strong": [
                    "we propose", "state-of-the-art", "our method", "baseline",
                    "appendix", "supplementary", "ablation", "significant", "p<",
                    "accuracy", "precision", "recall", "f1-score", "auc"
                ],
                "weak": [
                    "future work", "limitations", "materials", "proof", "lemma",
                    "corollary", "theorem"
                ],
            },
            "technical_spec": {
                "core": [
                    "specification", "requirements", "compliance", "scope",
                    "definitions", "normative", "non-normative", "shall", "must",
                    "should", "version"
                ],
                "strong": [
                    "must", "should", "may", "endpoint", "protocol", "field",
                    "schema", "message", "rfc", "request", "response"
                ],
                "weak": [
                    "example", "note", "informative", "optional"
                ],
            },
            "tutorial": {
                "core": [
                    "tutorial", "walkthrough", "step-by-step", "follow these steps",
                    "in this guide", "you will learn", "prerequisites", "getting started"
                ],
                "strong": [
                    "step 1", "step 2", "next,", "now,", "run the following",
                    "output", "screenshot", "tip", "warning", "note"
                ],
                "weak": [
                    "conclusion", "summary", "exercise"
                ],
            },
            "api_reference": {
                "core": [
                    "parameters", "returns", "raises", "examples", "deprecated",
                    "default", "type", "response", "request", "http", "endpoint",
                    "json", "status code", "query", "path", "body"
                ],
                "strong": [
                    "get", "post", "put", "delete", "200 ok", "404", "500",
                    "bearer", "authorization", "content-type", "application/json",
                    "schema", "field", "enum", "curl"
                ],
                "weak": [
                    "version", "sdk", "client", "rate limit"
                ],
            },
            "meeting_minutes": {
                "core": [
                    "attendees", "agenda", "minutes", "action items", "decisions",
                    "discussion", "next meeting", "timestamp", "meeting"
                ],
                "strong": [
                    "motion", "seconded", "carried", "meeting called to order",
                    "adjourned", "approved", "minutes of"
                ],
                "weak": [
                    "apologies", "chair", "secretary"
                ],
            },
            "legal_contract": {
                "core": [
                    "whereas", "hereinafter", "party", "agreement", "term",
                    "termination", "governing law", "indemnify", "liability",
                    "confidentiality", "warranty", "force majeure", "arbitration"
                ],
                "strong": [
                    "in witness whereof", "severability", "entire agreement",
                    "counterparts", "assigns", "notwithstanding"
                ],
                "weak": [
                    "thereof", "hereof", "hereto", "therein"
                ],
            },
            "news_article": {
                "core": [
                    "according to", "spokesperson", "reported", "announced",
                    "press release", "officials said", "on monday", "on tuesday",
                    "on wednesday", "on thursday", "on friday", "on saturday", "on sunday",
                    "said"
                ],
                "strong": [
                    "reuters", "associated press", "ap", "bbc", "cnn",
                    "as of", "breaking"
                ],
                "weak": [
                    "experts say", "sources say", "reporters"
                ],
            },
            "blog_post": {
                "core": [
                    "in this post", "today i", "i think", "my experience",
                    "we're going to", "thoughts", "opinion", "subscribe", "comments"
                ],
                "strong": [
                    "newsletter", "share", "like", "follow me", "personal", "thanks for reading"
                ],
                "weak": [
                    "wrap up", "behind the scenes", "challenges"
                ],
            },
        }

        base_scores: Dict[str, float] = {}
        for doc_type, indicators in doc_indicators.items():
            base_scores[doc_type] = self._calculate_weighted_score(
                lc, indicators)

        # Auxiliary semantic features
        alg_density = self._calculate_algorithm_density(lc)
        concept_complexity = self._calculate_concept_complexity(lc)
        impl_detail = self._calculate_implementation_detail_level(lc)

        # Additional semantic heuristics
        def pronoun_ratio(text: str) -> float:
            tokens = re.findall(r"[a-z]+", text)
            if not tokens:
                return 0.0
            prons = {"i", "my", "me", "mine", "we", "our", "ours", "us"}
            hits = sum(1 for t in tokens if t in prons)
            return min(1.0, hits / max(1, len(tokens)) * 8.0)

        def month_presence(text: str) -> float:
            months = [
                "january", "february", "march", "april", "may", "june",
                "july", "august", "september", "october", "november", "december"
            ]
            hits = sum(1 for m in months if m in text)
            return min(1.0, hits / 3.0)

        p_ratio = pronoun_ratio(lc)
        m_ratio = month_presence(lc)
        time_count = len(re.findall(r"\b\d{1,2}:\d{2}\b", lc))

        adjusted_scores: Dict[str, float] = {}
        for k, v in base_scores.items():
            m = 1.0
            if k == "research_paper":
                m *= (0.85 + 0.25 * concept_complexity)
                m *= (0.95 + 0.1 * (1.0 - impl_detail))
            elif k == "technical_spec":
                m *= (0.8 + 0.35 * impl_detail)
                m *= (0.95 + 0.1 * (1.0 - p_ratio))
            elif k == "tutorial":
                m *= (0.85 + 0.2 * alg_density + 0.15 * p_ratio)
            elif k == "api_reference":
                m *= (0.75 + 0.45 * impl_detail + 0.1 * alg_density)
            elif k == "meeting_minutes":
                time_boost = min(1.0, time_count / 3.0)
                m *= (0.8 + 0.25 * time_boost)
            elif k == "legal_contract":
                m *= (0.85 + 0.2 * (1.0 - alg_density))
            elif k == "news_article":
                m *= (0.85 + 0.25 * m_ratio)
            elif k == "blog_post":
                m *= (0.8 + 0.35 * p_ratio)
            adjusted_scores[k] = max(0.0, min(1.0, v * m))

        if not adjusted_scores:
            return ("unknown", 0.0)

        ranked = sorted(adjusted_scores.items(),
                        key=lambda x: x[1], reverse=True)
        top_type, top_score = ranked[0]
        second = ranked[1][1] if len(ranked) > 1 else 0.0
        separation = max(0.0, top_score - second)

        confidence = max(0.0, min(1.0, 0.4 * top_score +
                         0.6 * min(1.0, separation * 2.0)))
        return (top_type if top_score >= 0.15 else "unknown", confidence if top_score >= 0.15 else 0.0)

    def _calculate_weighted_score(self, content: str, indicators: Dict[str, List[str]]) -> float:
        '''Calculate weighted semantic indicator scores'''
        tiers = {
            "core": 0.5,
            "strong": 0.3,
            "weak": 0.2,
        }
        score = 0.0
        weight_sum = 0.0
        for tier, weight in tiers.items():
            patterns = indicators.get(tier, [])
            if not patterns:
                continue
            s = self._detect_pattern_score(content, patterns)
            score += weight * s
            weight_sum += weight
        if weight_sum == 0:
            return 0.0
        return max(0.0, min(1.0, score / weight_sum))

    def _detect_pattern_score(self, content: str, patterns: List[str]) -> float:
        '''Detect semantic pattern matching scores'''
        if not patterns:
            return 0.0

        def occurrence_count(text: str, pat: str) -> int:
            p = pat.strip().lower()
            if not p:
                return 0
            # Word or phrase
            if re.fullmatch(r"[a-z0-9_\-]+", p):
                # Single token-like
                return len(re.findall(rf"\b{re.escape(p)}\b", text))
            else:
                # Phrase: allow substring matches with word boundary on first/last alnum chars if present
                # Fallback to simple count
                return text.count(p)

        total = 0
        matched = 0
        for p in patterns:
            cnt = occurrence_count(content, p)
            total += 1
            if cnt > 0:
                matched += 1

        coverage = matched / total if total else 0.0

        # Frequency factor: more occurrences -> higher score, saturated
        freq_total = sum(max(0, min(5, occurrence_count(content, p)))
                         for p in patterns)
        freq_norm = min(1.0, freq_total / (len(patterns) * 3.0))

        # Combine coverage and frequency
        score = 0.6 * coverage + 0.4 * freq_norm
        return max(0.0, min(1.0, score))

    def detect_segmentation_strategy(self, content: str, doc_type: str) -> str:
        '''
        Intelligently determine the best segmentation strategy based on content semantics rather than mechanical structure
        '''
        text = (content or "").strip().lower()
        if not text:
            return "paragraphs"

        alg = self._calculate_algorithm_density(text)
        complexity = self._calculate_concept_complexity(text)
        impl = self._calculate_implementation_detail_level(text)
        tokens = re.findall(r"[a-z0-9]+", text)
        n_tokens = len(tokens)

        if doc_type == "research_paper":
            if alg >= 0.45:
                return "hybrid: semantic_sections + algorithmic_blocks"
            return "semantic_sections"
        if doc_type == "technical_spec":
            if impl >= 0.6:
                return "api_endpoints"
            return "semantic_sections"
        if doc_type == "api_reference":
            return "api_endpoints"
        if doc_type == "tutorial":
            if alg >= 0.5:
                return "code_snippets"
            return "conceptual_modules"
        if doc_type == "meeting_minutes":
            return "bullet_points"
        if doc_type == "legal_contract":
            return "legal_clauses"
        if doc_type == "news_article":
            return "news_paragraphs"
        if doc_type == "blog_post":
            return "paragraphs"

        # Fallback based on metrics
        if alg >= 0.55:
            return "code_snippets"
        if impl >= 0.6:
            return "api_endpoints"
        if complexity >= 0.6 and n_tokens > 400:
            return "semantic_sections"
        return "paragraphs"

    def _calculate_algorithm_density(self, content: str) -> float:
        '''Calculate algorithm content density'''
        algo_tokens = {
            "algorithm", "pseudocode", "time complexity", "o(", "o(n", "o(n^", "o(n log n",
            "space complexity", "runtime", "loop", "iterate", "iteration", "recursion",
            "recursive", "base case", "heap", "stack", "queue", "graph", "tree", "bfs",
            "dfs", "dp", "dynamic programming", "greedy", "sort", "sorted", "merge sort",
            "quick sort", "binary search", "hash", "map", "set", "pointer", "bitmask",
            "optimize", "optimization"
        }
        code_markers = [
            r"\bdef\b", r"\bclass\b", r"\bfunction\b", r"\bvar\b", r"\blet\b",
            r"::", r"->", r"=>", r"\{", r"\}", r";", r"`", r"```", r"\breturn\b",
            r"\bif\b", r"\belse\b", r"\bfor\b", r"\bwhile\b"
        ]

        tokens = re.findall(r"[a-z0-9\(\)\[\]\{\}\-_\.\+\*/=<>!]+", content)
        n_tokens = max(1, len(tokens))

        # Count algorithmic keywords (phrase-aware)
        algo_hits = 0
        for tok in algo_tokens:
            if " " in tok or "(" in tok:
                algo_hits += content.count(tok)
            else:
                algo_hits += len(re.findall(rf"\b{re.escape(tok)}\b", content))

        code_hits = sum(len(re.findall(p, content)) for p in code_markers)

        # Normalize per token count; saturate
        density = (algo_hits * 1.0 + code_hits * 0.6) / (n_tokens / 50.0 + 5.0)
        return max(0.0, min(1.0, density))

    def _calculate_concept_complexity(self, content: str) -> float:
        '''Calculate concept complexity'''
        # Sentence-based stats
        sentences = re.split(r"[.!?\n]+", content)
        sentences = [s.strip() for s in sentences if s.strip()]
        tokens = re.findall(r"[a-z]+", content)

        avg_len = 0.0
        if sentences:
            avg_len = sum(len(re.findall(r"[a-z]+", s))
                          for s in sentences) / len(sentences)

        # Normalize average sentence length between 10 and 35 words
        sent_norm = 0.0
        if avg_len > 0:
            sent_norm = max(0.0, min(1.0, (avg_len - 10.0) / 25.0))

        # Type-token ratio (vocabulary diversity)
        ttr = 0.0
        if tokens:
            unique = len(set(tokens))
            ttr_raw = unique / len(tokens)
            ttr = max(0.0, min(1.0, (ttr_raw - 0.2) / 0.4))  # 0.2..0.6 -> 0..1

        # Abstract terminology presence
        abstract_terms = [
            "theoretical", "proof", "lemma", "corollary", "framework",
            "architecture", "conceptual", "paradigm", "formal", "stochastic",
            "deterministic", "approximation", "generalization", "regularization",
            "convergence", "manifold", "hypothesis", "axiom", "inference"
        ]
        abs_hits = sum(1 for t in abstract_terms if t in content)
        abs_norm = max(0.0, min(1.0, abs_hits / 6.0))

        complexity = 0.4 * sent_norm + 0.3 * ttr + 0.3 * abs_norm
        return max(0.0, min(1.0, complexity))

    def _calculate_implementation_detail_level(self, content: str) -> float:
        '''Calculate implementation detail level'''
        # Indicators of implementation details: parameters, types, code, endpoints, configs
        param_markers = [
            "parameter", "parameters", "arg", "args", "kwargs", "returns", "raises",
            "default", "type", "bool", "int", "string", "float", "list", "dict",
            "class", "function", "method", "module"
        ]
        http_markers = [
            "http", "https", "endpoint", "request", "response", "status code",
            "get", "post", "put", "delete", "/v1/", "/api/", "application/json",
            "content-type", "authorization", "bearer"
        ]
        config_markers = [
            "config", "configuration", "settings", "option", "flag", "yaml", "json",
            "ini", "toml", "env", "environment variable", "path"
        ]
        code_patterns = [
            r"\bdef\b", r"\bclass\b", r"\bimport\b", r"\bfrom\b.*\bimport\b", r"::", r"->", r"=>",
            r"```\w*", r"`[a-z0-9_]+`", r"\{.*\}", r"\[.*\]", r"\(.*\)"
        ]

        text = content
        tokens = re.findall(r"[a-z0-9]+", text)
        n_tokens = max(1, len(tokens))

        def count_list_markers(lst: List[str]) -> int:
            c = 0
            for m in lst:
                if " " in m or "/" in m or "." in m:
                    c += text.count(m)
                else:
                    c += len(re.findall(rf"\b{re.escape(m)}\b", text))
            return c

        cnt_params = count_list_markers(param_markers)
        cnt_http = count_list_markers(http_markers)
        cnt_config = count_list_markers(config_markers)
        cnt_code = sum(len(re.findall(pat, text)) for pat in code_patterns)

        score = (cnt_params * 0.35 + cnt_http * 0.35 + cnt_config *
                 0.2 + cnt_code * 0.3) / (n_tokens / 60.0 + 6.0)
        return max(0.0, min(1.0, score))
