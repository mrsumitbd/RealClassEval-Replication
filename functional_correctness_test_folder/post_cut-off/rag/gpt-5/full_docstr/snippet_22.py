import math
import re
from typing import Dict, List, Tuple


class DocumentAnalyzer:
    '''Enhanced document analyzer using semantic content analysis instead of mechanical structure detection'''

    def analyze_document_type(self, content: str) -> Tuple[str, float]:
        '''
        Enhanced document type analysis based on semantic content patterns
        Returns:
            Tuple[str, float]: (document_type, confidence_score)
        '''
        text = content or ""
        text_l = text.lower()

        if not text_l.strip():
            return ("unknown", 0.0)

        # Semantic indicators per doc type
        doc_type_indicators: Dict[str, Dict[str, List[str]]] = {
            "research_paper": {
                "strong": [
                    r'\babstract\b', r'\bintroduction\b', r'\bmethod(s)?\b', r'\bresults?\b',
                    r'\bdiscussion\b', r'\bconclusion(s)?\b', r'\bexperiments?\b',
                    r'\btheorem\b', r'\blemma\b', r'\bproof\b', r'\bcomplexity\b',
                    r'\bwe propose\b', r'\bappendix\b', r'\breferences\b',
                ],
                "medium": [
                    r'\brelated work\b', r'\bdataset\b', r'\bevaluation\b', r'state[- ]of[- ]the[- ]art',
                    r'\bbaseline(s)?\b', r'\bdoi\b', r'\bfig\.\b', r'\btable\b',
                ],
                "weak": [r'\balgorithm\b', r'\bobjective\b', r'\boptimization\b'],
                "negative": [r'\bterms and conditions\b', r'\bprivacy policy\b', r'\blicense agreement\b'],
            },
            "tutorial": {
                "strong": [
                    r'\bstep[- ]by[- ]step\b', r'\bgetting started\b', r'\bprerequisites\b',
                    r'\binstall\b', r'\bpip install\b', r'\bexample(s)?\b', r'\bwalkthrough\b', r'\bguide\b',
                    r'\bnote:\b', r'\btip:\b',
                ],
                "medium": [
                    r'\bin this tutorial\b', r'\bwe will\b', r'\bhow to\b', r"\blet['’]s\b", r'\bquickstart\b',
                    r'\btry it\b',
                ],
                "weak": [r'\bexercise\b', r'\bpractice\b', r'\btips\b'],
                "negative": [r'\btheorem\b', r'\blemma\b', r'\bproof\b', r'\bhereby\b', r'\bshall\b'],
            },
            "api_reference": {
                "strong": [
                    r'\bparameters?\b', r'\breturns?\b', r'\braises\b', r'\bsignature\b', r'\bdeprecated\b',
                    r'\bdefault\b', r'\btype(s)?:\b', r'\battributes?\b', r'\bsee also\b',
                    r'\bmodule\b', r'\bclass\b', r'\bmethod\b', r'\bproperty\b',
                ],
                "medium": [
                    r'\bsyntax\b', r'\barguments?\b', r'\bkwargs\b', r'\boverload\b',
                    r'\bnamespace\b', r'\bpackage\b', r'\bimport\b', r'\breturns?\b',
                ],
                "weak": [r'\bdef\b', r'\bclass\b', r'\bpublic\b', r'\bstatic\b', r'\bvoid\b'],
                "negative": [r'\bintroduction\b', r'\bwe propose\b', r'\bstory\b'],
            },
            "specification": {
                "strong": [
                    r'\bRFC\b', r'\bMUST\b', r'\bSHOULD\b', r'\bMAY\b', r'\bMUST NOT\b', r'\bSHALL\b',
                    r'\bconformance\b', r'\bcompliance\b', r'\bnormative\b', r'\bnon[- ]normative\b',
                    r'\brequirements?\b',
                ],
                "medium": [r'\bscope\b', r'\bdefinitions?\b', r'\bterminology\b', r'\bsecurity considerations\b'],
                "weak": [r'\bappendix\b', r'\bABNF\b', r'\bgrammar\b'],
                "negative": [r'\bstory\b', r'\bblog\b'],
            },
            "design_doc": {
                "strong": [
                    r'\bdesign\b', r'\bmotivation\b', r'\btrade[- ]offs\b', r'\balternatives?\b', r'\brationale\b',
                    r'\bnon[- ]goals?\b', r'\bassumptions?\b', r'\brisks?\b', r'\barchitecture\b', r'\bcomponents?\b',
                ],
                "medium": [r'\bdecision\b', r'\bpros\b', r'\bcons\b', r'\bimpact\b', r'\bfuture work\b'],
                "weak": [r'\bdiagram\b', r'\boverview\b'],
                "negative": [r'\blegal\b', r'\bshall\b'],
            },
            "meeting_minutes": {
                "strong": [
                    r'\bagenda\b', r'\battendees\b', r'\baction items?\b', r'\bmeeting\b', r'\bminutes\b',
                    r'\bdiscussion\b', r'\bnext steps?\b', r'\bfollow[- ]up\b', r'\bdecisions?\b',
                ],
                "medium": [r'\b\d{1,2}:\d{2}\b', r'\b\d{4}-\d{2}-\d{2}\b', r'\bvote\b'],
                "weak": [r'\bnote(s)?\b', r'\bsummary\b'],
                "negative": [r'\btheorem\b', r'\bapi\b'],
            },
            "news_article": {
                "strong": [
                    r'\baccording to\b', r'\bsaid\b', r'\breported\b', r'\bannounced\b', r'\bofficial\b',
                    r'\bspokesperson\b', r'\bagency\b', r'\bbreaking\b', r'\binterview\b',
                ],
                "medium": [r'\bReuters\b', r'\bAP\b', r'\bBBC\b', r'\bCNN\b', r'\bDate:\b'],
                "weak": [r'\bphoto\b', r'\bcaption\b', r'\bupdate\b'],
                "negative": [r'\btheorem\b', r'\bapi\b'],
            },
            "legal_contract": {
                "strong": [
                    r'\bagreement\b', r'\bparty(ies)?\b', r'\bgoverning law\b', r'\bhereby\b', r'\bthereof\b',
                    r'\bhereto\b', r'\bindemnif(y|ication)\b', r'\bliab(le|ility)\b', r'\bforce majeure\b',
                    r'\bwarranty\b', r'\bconfidentiality\b', r'\btermination\b', r'\bassignment\b',
                    r'\bclause\b', r'\bwhereas\b', r'\bwitnesseth\b', r'\bshall\b',
                ],
                "medium": [r'\beffective date\b', r'\bcounterpart(s)?\b', r'\bseverability\b', r'\bjurisdiction\b'],
                "weak": [r'\bnotwithstanding\b', r'\bherein\b'],
                "negative": [r'\bappendix\b', r'\bcode\b'],
            },
            "technical_report": {
                "strong": [
                    r'\bexecutive summary\b', r'\bmethodology\b', r'\bfindings?\b', r'\banalysis\b', r'\bresults?\b',
                    r'\brecommendations?\b', r'\bappendix\b', r'\breferences\b',
                ],
                "medium": [r'\babstract\b', r'\bintroduction\b', r'\bconclusion(s)?\b', r'\bdata\b'],
                "weak": [r'\bfigure\b', r'\btable\b'],
                "negative": [r'\bblog\b', r'\bstory\b'],
            },
            "blog_post": {
                "strong": [
                    r'\bI\b', r'\bwe\b', r'\bour\b', r'\bstory\b', r'\btoday\b', r'\bthoughts\b', r'\bopinion\b',
                    r'\bsubscribe\b', r'\bcomments\b', r'\bauthor\b', r'\bposted on\b', r'\bupdate\b',
                ],
                "medium": [r'\bin this post\b', r'\bshare\b', r'\bjourney\b', r'\blessons\b', r'\bbehind the scenes\b'],
                "weak": [r'\bimage\b', r'\blikes\b', r'\bfollowers\b'],
                "negative": [r'\bMUST\b', r'\bSHALL\b'],
            },
        }

        # Compute base semantic scores
        base_scores: Dict[str, float] = {}
        for doc_type, indicators in doc_type_indicators.items():
            base_scores[doc_type] = self._calculate_weighted_score(
                text_l, indicators)

        # Content metrics
        alg_density = self._calculate_algorithm_density(text_l)
        concept_complexity = self._calculate_concept_complexity(text_l)
        impl_detail = self._calculate_implementation_detail_level(text)

        # Refine scores based on content metrics
        refined_scores: Dict[str, float] = {}
        for doc_type, score in base_scores.items():
            s = score
            if doc_type == "research_paper":
                s += 0.20 * alg_density + 0.20 * concept_complexity - 0.10 * impl_detail
            elif doc_type == "tutorial":
                s += 0.20 * impl_detail + 0.10 * (1.0 - concept_complexity)
            elif doc_type == "api_reference":
                s += 0.30 * impl_detail + 0.10 * (1.0 - concept_complexity)
            elif doc_type == "specification":
                s += 0.15 * concept_complexity - 0.10 * impl_detail
            elif doc_type == "design_doc":
                s += 0.10 * concept_complexity + 0.10 * impl_detail
            elif doc_type == "meeting_minutes":
                s += 0.10 * (1.0 - concept_complexity) - 0.05 * impl_detail
            elif doc_type == "news_article":
                s += 0.10 * (1.0 - concept_complexity)
            elif doc_type == "legal_contract":
                s += 0.20 * concept_complexity - 0.15 * impl_detail
            elif doc_type == "technical_report":
                s += 0.15 * concept_complexity + 0.10 * alg_density
            elif doc_type == "blog_post":
                s += 0.15 * (1.0 - concept_complexity)

            refined_scores[doc_type] = max(0.0, min(1.0, s))

        # Select best type and compute confidence
        sorted_types = sorted(refined_scores.items(),
                              key=lambda kv: kv[1], reverse=True)
        best_type, best_score = sorted_types[0]
        second_score = sorted_types[1][1] if len(sorted_types) > 1 else 0.0

        token_count = max(1, len(re.findall(r'\w+', text_l)))
        # shorter docs -> lower confidence
        length_factor = min(1.0, math.log1p(token_count) / 5.0)

        confidence_gap = best_score - second_score
        confidence = 0.5 + 0.8 * confidence_gap
        confidence = max(0.0, min(0.99, confidence * length_factor))

        return best_type, confidence

    def _calculate_weighted_score(self, content: str, indicators: Dict[str, List[str]]) -> float:
        '''Calculate weighted semantic indicator scores'''
        if not indicators:
            return 0.0

        weight_map: Dict[str, float] = {
            "strong": 3.0,
            "medium": 2.0,
            "weak": 1.0,
            "bonus": 1.5,
            "penalty": -1.5,
            "negative": -2.5,
        }

        s = 0.0
        for key, patterns in indicators.items():
            # Allow numeric weight keys as strings (e.g., "2.5")
            try:
                weight = float(key)
            except ValueError:
                weight = weight_map.get(key, 1.0)
            grp_score = self._detect_pattern_score(content, patterns)
            s += weight * grp_score

        # Normalize using logistic to keep within 0..1
        normalized = 1.0 / (1.0 + math.exp(-s))
        return normalized

    def _detect_pattern_score(self, content: str, patterns: List[str]) -> float:
        '''Detect semantic pattern matching scores'''
        if not patterns:
            return 0.0

        text = content or ""
        token_count = max(1, len(re.findall(r'\w+', text)))
        norm_units = max(1.0, token_count / 200.0)

        total_occ = 0.0
        for pat in patterns:
            try:
                total_occ += len(re.findall(pat, text,
                                 flags=re.IGNORECASE | re.MULTILINE))
            except re.error:
                safe_pat = re.escape(pat)
                total_occ += len(re.findall(safe_pat, text,
                                 flags=re.IGNORECASE | re.MULTILINE))

        frequency = total_occ / norm_units  # occurrences per ~200 tokens
        score = 1.0 - math.exp(-frequency)  # bounded in [0,1)
        return max(0.0, min(1.0, score))

    def detect_segmentation_strategy(self, content: str, doc_type: str) -> str:
        '''
        Intelligently determine the best segmentation strategy based on content semantics rather than mechanical structure
        '''
        text = content or ""
        doc_type = (doc_type or "").lower()

        alg_density = self._calculate_algorithm_density(text)
        concept_complexity = self._calculate_concept_complexity(text)
        impl_detail = self._calculate_implementation_detail_level(text)

        if doc_type in {"api_reference"} or impl_detail > 0.70:
            return "code_blocks"

        if doc_type in {"research_paper", "technical_report"}:
            if alg_density > 0.60:
                return "algorithm_steps"
            return "semantic_sections"

        if doc_type in {"tutorial", "blog_post"}:
            if impl_detail >= 0.50:
                return "hybrid_semantic"
            return "paragraphs"

        if doc_type in {"specification", "legal_contract"}:
            return "requirements"

        if doc_type in {"design_doc"}:
            return "semantic_sections"

        # Fallback based on metrics
        if concept_complexity > 0.60:
            return "semantic_sections"
        if impl_detail > 0.50:
            return "code_blocks"
        if alg_density > 0.55:
            return "algorithm_steps"
        return "paragraphs"

    def _calculate_algorithm_density(self, content: str) -> float:
        '''Calculate algorithm content density'''
        text = content or ""
        patterns = [
            r'\balgorithm\b', r'\bruntime\b', r'\btime complexity\b', r'O\(', r'\bNP[- ](hard|complete)\b',
            r'\btheorem\b', r'\blemma\b', r'\bproof\b', r'\bproposition\b', r'\bcorollary\b',
            r'\bdefinition\b', r'\binvariant\b', r'\binduction\b', r'\bprocedure\b',
            r'^\s*\d+\.\s',  # numbered steps
            r'\binput:\b', r'\boutput:\b',
        ]
        base = self._detect_pattern_score(text, patterns)

        # Additional boost for math symbols
        math_symbols = [r'∑', r'∫', r'≥', r'≤', r'⇒', r'∈', r'∀', r'∃']
        math_score = self._detect_pattern_score(text, math_symbols) * 0.5

        score = base + math_score
        return max(0.0, min(1.0, score))

    def _calculate_concept_complexity(self, content: str) -> float:
        '''Calculate concept complexity'''
        text = content or ""
        tokens = re.findall(r"[A-Za-z]+", text)
        n = len(tokens)
        if n == 0:
            return 0.0

        long_words = sum(1 for t in tokens if len(t) >= 8)
        frac_long = long_words / n

        unique_ratio = len(set(t.lower() for t in tokens)) / n

        advanced_vocab = [
            r'\btheoretical\b', r'\bframework\b', r'\barchitecture\b', r'\bparadigm\b', r'\bsemantics?\b',
            r'\bepistemology\b', r'\baxiom(s)?\b', r'\bontology\b', r'\bformal(ism|ization)?\b',
            r'\basymptotic\b', r'\bmanifold\b', r'\bgradient\b', r'\bhessian\b',
        ]
        adv_score = self._detect_pattern_score(text, advanced_vocab)

        # Complexity from average word length
        avg_len = sum(len(t) for t in tokens) / n
        # maps ~4.5..10.5 -> 0..1
        len_score = max(0.0, min(1.0, (avg_len - 4.5) / 6.0))

        # Combine
        score = 0.4 * frac_long + 0.3 * adv_score + 0.2 * len_score + 0.1 * unique_ratio
        return max(0.0, min(1.0, score))

    def _calculate_implementation_detail_level(self, content: str) -> float:
        '''Calculate implementation detail level'''
        text = content or ""
        code_patterns = [
            r'```', r'~~~', r'^\s*#include\b', r'^\s*using\s', r'^\s*import\b', r'^\s*from\s+\w+\s+import\b',
            r'^\s*def\s+\w+\(', r'^\s*class\s+\w+', r'^\s*public\s', r'^\s*private\s', r'^\s*static\s',
            r'\bfunction\s*\(', r'\bvar\s+\w+', r'\blet\s+\w+', r'\bconst\s+\w+', r';\s*$', r'\{|\}',
            r'\bSELECT\b', r'\bINSERT\b', r'\bUPDATE\b', r'\bDELETE\b', r'^\s*\$\s',  # shell
            r'^\s*curl\s', r'^\s*git\s', r'\bJSON\b', r'\bYAML\b',
        ]
        base = self._detect_pattern_score(text, code_patterns)

        # Code-like line ratio
        lines = [ln for ln in text.splitlines() if ln.strip() != ""]
        total_lines = max(1, len(lines))
        codey = 0
        code_line_regexes = [
            re.compile(r'^\s{2,}\S'),  # indented
            re.compile(r'.*[{;}].*$'),
            re.compile(r'^\s*(def|class|import|from|if|for|while|try|catch)\b'),
        ]
        for ln in lines:
            if any(rgx.search(ln) for rgx in code_line_regexes):
                codey += 1
        ratio = codey / total_lines

        score = max(0.0, min(1.0, base * 0.7 + ratio * 0.6))
        return score
