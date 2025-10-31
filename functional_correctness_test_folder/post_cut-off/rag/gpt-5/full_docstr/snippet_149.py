import json
import os
import re
from typing import Any, Dict, List, Optional, Tuple

try:
    import pandas as pd
except Exception:  # pragma: no cover
    pd = None  # type: ignore


class ArticleEvaluator:
    '''
    A class to evaluate the factual accuracy of AI-generated Wikipedia articles
    against reference articles using OpenAI models.
    '''

    def __init__(self, openai_api_key: Optional[str] = None, model: str = 'gpt-4o'):
        '''
        Initialize the ArticleEvaluator with API credentials and model settings.
        Args:
            openai_api_key: API key for OpenAI (falls back to OPENAI_API_KEY env var)
            model: The OpenAI model to use for evaluation (default: gpt-4o)
        '''
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        self.model = model

        self._client = None
        self._client_type = None  # 'v1' or 'legacy'
        # Try new SDK first
        try:
            from openai import OpenAI  # type: ignore
            self._client = OpenAI(
                api_key=self.openai_api_key) if self.openai_api_key else OpenAI()  # type: ignore
            self._client_type = 'v1'
        except Exception:
            # Fallback to legacy SDK
            try:
                import openai  # type: ignore
                openai.api_key = self.openai_api_key or os.getenv(
                    'OPENAI_API_KEY')
                self._client = openai
                self._client_type = 'legacy'
            except Exception:
                self._client = None
                self._client_type = None

    def get_reference_article(self, json_data: Dict, title: str) -> Optional[str]:
        '''
        Retrieve reference article text from the JSON data.
        Args:
            json_data: The loaded JSON data with Wikipedia articles
            title: The title of the article to retrieve
        Returns:
            The plain text content of the reference article, or None if not found
        '''
        def norm(s: str) -> str:
            return re.sub(r'\s+', ' ', s.strip()).casefold()

        def extract_text(obj: Dict) -> Optional[str]:
            text_keys = [
                'text', 'content', 'extract', 'plain_text', 'article', 'body', 'wiki_text', 'wikitext'
            ]
            for k in text_keys:
                v = obj.get(k)
                if isinstance(v, str) and v.strip():
                    return v
            # Common Wikipedia API shapes
            # e.g., {'parse': {'text': {'*': '...'}}}
            parse = obj.get('parse')
            if isinstance(parse, dict):
                text = parse.get('text')
                if isinstance(text, dict):
                    star = text.get('*')
                    if isinstance(star, str) and star.strip():
                        return star
            # Sections or paragraphs
            for key in ('sections', 'paragraphs'):
                arr = obj.get(key)
                if isinstance(arr, list):
                    parts = []
                    for item in arr:
                        if isinstance(item, dict):
                            for tk in ('text', 'content', 'body'):
                                tv = item.get(tk)
                                if isinstance(tv, str):
                                    parts.append(tv)
                    if parts:
                        return '\n\n'.join(parts).strip() or None
            # Revisions shape (MediaWiki)
            revisions = obj.get('revisions')
            if isinstance(revisions, list) and revisions:
                rev = revisions[0]
                if isinstance(rev, dict):
                    for tk in ('content', 'slots'):
                        val = rev.get(tk)
                        if isinstance(val, dict):
                            main = val.get('main')
                            if isinstance(main, dict):
                                wikitext = main.get(
                                    '*') or main.get('content') or main.get('text')
                                if isinstance(wikitext, str) and wikitext.strip():
                                    return wikitext
                    star = rev.get('*')
                    if isinstance(star, str) and star.strip():
                        return star
            return None

        wanted = norm(title)

        # Case 1: dict keyed by title directly
        if isinstance(json_data, dict):
            # Direct key
            if title in json_data and isinstance(json_data[title], str):
                return json_data[title]
            # Article container keys
            for container_key in ('articles', 'pages', 'items', 'data'):
                container = json_data.get(container_key)
                if isinstance(container, list):
                    for item in container:
                        if isinstance(item, dict):
                            t = item.get('title') or item.get(
                                'name') or item.get('page') or item.get('id')
                            if isinstance(t, str) and norm(t) == wanted:
                                txt = extract_text(item)
                                if txt:
                                    return txt
                elif isinstance(container, dict):
                    # MediaWiki 'query.pages'
                    if container_key == 'pages':
                        for _, page in container.items():
                            if isinstance(page, dict):
                                t = page.get('title') or page.get('name')
                                if isinstance(t, str) and norm(t) == wanted:
                                    txt = extract_text(page)
                                    if txt:
                                        return txt
                    else:
                        # Arbitrary dict of items
                        for _, item in container.items():
                            if isinstance(item, dict):
                                t = item.get('title') or item.get(
                                    'name') or item.get('page') or item.get('id')
                                if isinstance(t, str) and norm(t) == wanted:
                                    txt = extract_text(item)
                                    if txt:
                                        return txt
            # Top-level list-like in dict under unknown key names
            for k, v in json_data.items():
                if isinstance(v, list):
                    for item in v:
                        if isinstance(item, dict):
                            t = item.get('title') or item.get(
                                'name') or item.get('page') or item.get('id')
                            if isinstance(t, str) and norm(t) == wanted:
                                txt = extract_text(item)
                                if txt:
                                    return txt

        # Case 2: json_data is a list of article dicts
        if isinstance(json_data, list):
            for item in json_data:
                if isinstance(item, dict):
                    t = item.get('title') or item.get(
                        'name') or item.get('page') or item.get('id')
                    if isinstance(t, str) and norm(t) == wanted:
                        txt = extract_text(item)
                        if txt:
                            return txt

        return None

    def prepare_article_for_evaluation(self, article_content: str) -> Tuple[str, List[str]]:
        '''
        Prepare an AI-generated article for evaluation by numbering its lines.
        Args:
            article_content: The content of the AI-generated article
        Returns:
            A tuple containing:
            - Numbered article text suitable for the prompt
            - List of the original lines for further processing
        '''
        if not article_content:
            return "", []
        raw_lines = article_content.splitlines()
        # Keep non-empty trimmed lines
        lines = [ln.strip() for ln in raw_lines if ln.strip() != ""]
        numbered = "\n".join(
            [f"{i+1}: {line}" for i, line in enumerate(lines)])
        return numbered, lines

    def evaluate_article_accuracy(self, reference_content: str, generated_article: str, temperature: float = 0.2) -> Dict[str, Any]:
        '''
        Evaluate the factual accuracy of an AI-generated article against a reference.
        Args:
            reference_content: The text of the reference Wikipedia article
            generated_article: The text of the AI-generated article
            temperature: The sampling temperature for the OpenAI API call
        Returns:
            Dictionary containing the evaluation results
        '''
        if not reference_content or not generated_article:
            raise ValueError(
                "Both reference_content and generated_article must be provided.")

        numbered_article, original_lines = self.prepare_article_for_evaluation(
            generated_article)

        system_prompt = (
            "You are a careful fact-checker. Compare each numbered line of the AI-generated article "
            "against the provided reference article text. For each line, decide one label:\n"
            "- accurate: The claim is supported by the reference\n"
            "- inaccurate: The claim contradicts the reference\n"
            "- unverifiable: The claim is not present in the reference and cannot be verified\n"
            "- hallucination: The claim introduces false or fabricated information clearly not supported\n\n"
            "Return a strict, minified JSON object with keys: lines, overall_summary, overall_confidence. "
            "The 'lines' value must be a list of objects with keys: line_number (int), label (string), "
            "confidence (float between 0 and 1), justification (string, brief), and optional corrected_fact (string) "
            "for inaccurate or hallucination lines. Do not include any text outside the JSON."
        )

        user_prompt = (
            "REFERENCE ARTICLE:\n"
            "<<<\n"
            f"{reference_content}\n"
            ">>>\n\n"
            "AI-GENERATED ARTICLE (NUMBERED LINES):\n"
            "<<<\n"
            f"{numbered_article}\n"
            ">>>\n\n"
            "Now evaluate each line as specified."
        )

        if self._client is None or self._client_type is None:
            # Offline fallback: mark all unverifiable
            lines_eval = [{
                "line_number": i + 1,
                "label": "unverifiable",
                "confidence": 0.0,
                "justification": "OpenAI client unavailable; offline fallback.",
            } for i in range(len(original_lines))]
            return {
                "lines": lines_eval,
                "overall_summary": "Evaluation could not be performed; OpenAI client unavailable.",
                "overall_confidence": 0.0,
                "model": self.model,
                "numbered_article": numbered_article,
                "raw_response": None,
                "usage": None,
            }

        raw_content = ""
        usage = None

        if self._client_type == 'v1':
            # New SDK
            try:
                resp = self._client.chat.completions.create(
                    model=self.model,
                    temperature=temperature,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    response_format={"type": "json_object"},
                )
                raw_content = resp.choices[0].message.content or ""
                try:
                    usage = {
                        "prompt_tokens": getattr(resp.usage, "prompt_tokens", None),
                        "completion_tokens": getattr(resp.usage, "completion_tokens", None),
                        "total_tokens": getattr(resp.usage, "total_tokens", None),
                    }
                except Exception:
                    usage = None
            except Exception as e:
                raw_content = json.dumps({
                    "error": str(e),
                    "lines": [
                        {
                            "line_number": i + 1,
                            "label": "unverifiable",
                            "confidence": 0.0,
                            "justification": "Error during OpenAI call."
                        } for i in range(len(original_lines))
                    ],
                    "overall_summary": "Error during OpenAI call.",
                    "overall_confidence": 0.0
                })
        else:
            # Legacy SDK
            try:
                resp = self._client.ChatCompletion.create(
                    model=self.model,
                    temperature=temperature,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                )
                raw_content = resp["choices"][0]["message"]["content"] or ""
                usage = resp.get("usage")
            except Exception as e:
                raw_content = json.dumps({
                    "error": str(e),
                    "lines": [
                        {
                            "line_number": i + 1,
                            "label": "unverifiable",
                            "confidence": 0.0,
                            "justification": "Error during OpenAI call."
                        } for i in range(len(original_lines))
                    ],
                    "overall_summary": "Error during OpenAI call.",
                    "overall_confidence": 0.0
                })

        parsed = self._safe_parse_json(raw_content)

        lines = parsed.get("lines")
        if not isinstance(lines, list):
            # Attempt alternative keys or structures
            for key in ("evaluations", "line_evaluations", "items", "results"):
                cand = parsed.get(key)
                if isinstance(cand, list):
                    lines = cand
                    break
        if not isinstance(lines, list):
            # Fallback: produce unverifiable for each line
            lines = [{
                "line_number": i + 1,
                "label": "unverifiable",
                "confidence": 0.0,
                "justification": "Could not parse model output."
            } for i in range(len(original_lines))]

        normalized_lines = []
        for i, line_obj in enumerate(lines):
            if not isinstance(line_obj, dict):
                continue
            ln = line_obj.get("line_number")
            if not isinstance(ln, int):
                ln = i + 1
            label = line_obj.get("label") or line_obj.get(
                "status") or line_obj.get("classification") or "unverifiable"
            label = self._normalize_label(label)
            conf = line_obj.get("confidence")
            try:
                conf_f = float(conf)
            except Exception:
                conf_f = None
            if conf_f is None or not (0.0 <= conf_f <= 1.0):
                conf_f = 0.0
            justification = line_obj.get("justification") or line_obj.get(
                "explanation") or line_obj.get("reason") or ""
            corrected = line_obj.get(
                "corrected_fact") or line_obj.get("correction") or None

            # Attach original text if available
            text = original_lines[ln -
                                  1] if 1 <= ln <= len(original_lines) else None

            normalized_lines.append({
                "line_number": ln,
                "text": text,
                "label": label,
                "confidence": conf_f,
                "justification": justification,
                "corrected_fact": corrected
            })

        overall_summary = parsed.get(
            "overall_summary") or parsed.get("summary") or ""
        overall_confidence = parsed.get(
            "overall_confidence") or parsed.get("confidence") or 0.0
        try:
            overall_confidence = float(overall_confidence)
        except Exception:
            overall_confidence = 0.0
        if not (0.0 <= overall_confidence <= 1.0):
            overall_confidence = 0.0

        return {
            "lines": normalized_lines,
            "overall_summary": overall_summary,
            "overall_confidence": overall_confidence,
            "model": self.model,
            "numbered_article": numbered_article,
            "raw_response": raw_content,
            "usage": usage,
        }

    def calculate_accuracy_score(self, evaluation_data: Dict) -> float:
        '''
        Calculate a normalized accuracy score from evaluation data.
        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy
        Returns:
            A score between -1 and 1 for compatibility with existing scoring
        '''
        label_to_score = {
            "accurate": 1.0,
            "correct": 1.0,
            "supported": 1.0,
            "mostly_accurate": 0.75,
            "partially_accurate": 0.5,
            "partial": 0.5,
            "mixed": 0.25,
            "neutral": 0.0,
            "unverifiable": 0.0,
            "insufficient": 0.0,
            "unknown": 0.0,
            "inaccurate": -0.5,
            "unsupported": -0.5,
            "false": -1.0,
            "hallucination": -1.0,
            "fabricated": -1.0,
        }
        lines = evaluation_data.get("lines") or []
        scores: List[float] = []
        for item in lines:
            if not isinstance(item, dict):
                continue
            label = self._normalize_label(item.get("label"))
            score = label_to_score.get(label)
            if score is None:
                # default neutral if unknown
                score = 0.0
            scores.append(float(score))
        if not scores:
            return 0.0
        avg = sum(scores) / len(scores)
        return max(-1.0, min(1.0, avg))

    def calculate_accuracy_statistics(self, evaluation_data: Dict) -> Dict:
        '''
        Calculate statistics from the evaluation data.
        Args:
            evaluation_data: The line-by-line evaluation dictionary
        Returns:
            Dictionary with accuracy statistics
        '''
        lines = evaluation_data.get("lines") or []
        counts: Dict[str, int] = {}
        confidences: List[float] = []
        total = 0

        for item in lines:
            if not isinstance(item, dict):
                continue
            label = self._normalize_label(item.get("label"))
            counts[label] = counts.get(label, 0) + 1
            total += 1
            conf = item.get("confidence")
            try:
                cf = float(conf)
                if 0.0 <= cf <= 1.0:
                    confidences.append(cf)
            except Exception:
                pass

        accu = counts.get("accurate", 0)
        inac = counts.get("inaccurate", 0)
        hall = counts.get("hallucination", 0)
        unv = counts.get("unverifiable", 0)

        accuracy_rate = (accu / total) if total else 0.0
        error_rate = ((inac + hall) / total) if total else 0.0
        unverifiable_rate = (unv / total) if total else 0.0
        avg_confidence = (sum(confidences) / len(confidences)
                          ) if confidences else 0.0

        return {
            "counts": counts,
            "total_lines": total,
            "accuracy_rate": accuracy_rate,
            "error_rate": error_rate,
            "unverifiable_rate": unverifiable_rate,
            "average_confidence": avg_confidence,
            "score": self.calculate_accuracy_score(evaluation_data),
        }

    def evaluation_to_dataframe(self, evaluation_data: Dict) -> 'pd.DataFrame':
        '''
        Convert evaluation data to a pandas DataFrame for easier analysis.
        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy
        Returns:
            DataFrame with evaluation results
        '''
        if pd is None:
            raise RuntimeError(
                "pandas is required for evaluation_to_dataframe but is not installed.")
        lines = evaluation_data.get("lines") or []
        rows = []
        for item in lines:
            if not isinstance(item, dict):
                continue
            rows.append({
                "line_number": item.get("line_number"),
                "text": item.get("text"),
                "label": self._normalize_label(item.get("label")),
                "confidence": item.get("confidence"),
                "justification": item.get("justification"),
                "corrected_fact": item.get("corrected_fact"),
            })
        df = pd.DataFrame(rows, columns=[
                          "line_number", "text", "label", "confidence", "justification", "corrected_fact"])
        return df

    def _normalize_label(self, label: Any) -> str:
        if not isinstance(label, str):
            return "unverifiable"
        l = label.strip().lower()
        synonyms = {
            "accurate": {"accurate", "correct", "supported", "true"},
            "inaccurate": {"inaccurate", "incorrect", "unsupported", "contradicted"},
            "unverifiable": {"unverifiable", "not verifiable", "unknown", "insufficient", "cannot verify", "not found"},
            "hallucination": {"hallucination", "fabricated", "made up", "false"},
            "mostly_accurate": {"mostly accurate", "largely accurate"},
            "partially_accurate": {"partially accurate", "partial", "partially true"},
            "mixed": {"mixed"},
        }
        for canon, variants in synonyms.items():
            if l in variants:
                return canon
        return l

    def _safe_parse_json(self, text: str) -> Dict[str, Any]:
        if not text:
            return {}
        # Try direct parse
        try:
            return json.loads(text)
        except Exception:
            pass
        # Extract JSON code block
        m = re.search(r"```(?:json)?\s*(\{[\s\S]*?\})\s*```", text)
        if m:
            try:
                return json.loads(m.group(1))
            except Exception:
                pass
        # Find first JSON object
        m2 = re.search(r"(\{[\s\S]*\})", text)
        if m2:
            snippet = m2.group(1)
            # Try to balance braces by trimming trailing garbage
            last_brace = snippet.rfind('}')
            if last_brace != -1:
                try:
                    return json.loads(snippet[:last_brace+1])
                except Exception:
                    pass
        # As a last resort, return empty dict
        return {}
