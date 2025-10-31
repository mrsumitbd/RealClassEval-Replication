from typing import Optional, Dict, List, Tuple, Any
import os
import re
import json
import pandas as pd

try:
    from openai import OpenAI
except Exception:
    OpenAI = None  # type: ignore


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
        self.api_key = openai_api_key or os.environ.get("OPENAI_API_KEY")
        self.model = model
        self._client = None
        if self.api_key and OpenAI is not None:
            try:
                self._client = OpenAI(api_key=self.api_key)
            except Exception:
                self._client = None

    def get_reference_article(self, json_data: Dict, title: str) -> Optional[str]:
        '''
        Retrieve reference article text from the JSON data.
        Args:
            json_data: The loaded JSON data with Wikipedia articles
            title: The title of the article to retrieve
        Returns:
            The plain text content of the reference article, or None if not found
        '''
        if not isinstance(json_data, dict) or not title:
            return None

        normalized = title.strip().lower()

        # Common structures:
        # 1) {"articles": [{"title": "...", "text": "..."}, ...]}
        # 2) {"Title": {"content": "..."}}
        # 3) {"Title": "full text..."}
        # 4) {"pages": {"Title": {"plain_text": "..."}}}
        candidates = []

        def extract_text(obj: Any) -> Optional[str]:
            if obj is None:
                return None
            if isinstance(obj, str):
                return obj.strip() or None
            if isinstance(obj, dict):
                for key in ("plain_text", "text", "content", "body", "article", "wiki_text"):
                    if key in obj and isinstance(obj[key], str):
                        if obj[key].strip():
                            return obj[key].strip()
            return None

        # Case 1 and 4
        for container_key in ("articles", "pages", "data", "items"):
            if container_key in json_data:
                container = json_data[container_key]
                if isinstance(container, dict):
                    for k, v in container.items():
                        if isinstance(k, str) and k.strip().lower() == normalized:
                            txt = extract_text(v)
                            if txt:
                                candidates.append(txt)
                elif isinstance(container, list):
                    for item in container:
                        if isinstance(item, dict):
                            t = item.get("title") or item.get(
                                "name") or item.get("page")
                            if isinstance(t, str) and t.strip().lower() == normalized:
                                txt = extract_text(item) or extract_text(
                                    item.get("content"))  # type: ignore
                                if txt:
                                    candidates.append(txt)

        # Direct top-level keyed by title
        if not candidates:
            for k, v in json_data.items():
                if isinstance(k, str) and k.strip().lower() == normalized:
                    txt = extract_text(v)
                    if txt:
                        candidates.append(txt)

        # Heuristic: among candidates, pick longest
        if candidates:
            return max(candidates, key=len)

        # Fallback: search list of dicts
        if isinstance(json_data, list):
            for item in json_data:
                if isinstance(item, dict):
                    t = item.get("title") or item.get(
                        "name") or item.get("page")
                    if isinstance(t, str) and t.strip().lower() == normalized:
                        txt = extract_text(item)
                        if txt:
                            return txt

        return None

    def prepare_article_for_evaluation(self, article_content: str) -> Tuple[str, List[str]]:
        cleaned = self._clean_text(article_content or "")
        sentences = self._split_into_sentences(cleaned)
        return cleaned, sentences

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
        ref_clean, _ = self.prepare_article_for_evaluation(
            reference_content or "")
        gen_clean, gen_sentences = self.prepare_article_for_evaluation(
            generated_article or "")

        result: Dict[str, Any] = {
            "model": self.model,
            "temperature": temperature,
            "reference_length": len(ref_clean),
            "generated_length": len(gen_clean),
            "sentences": gen_sentences,
            "evaluations": [],
            "raw_response": None,
            "error": None,
        }

        if not gen_sentences:
            result["error"] = "No sentences to evaluate."
            return result

        if not ref_clean:
            # If no reference, mark all as uncertain
            evaluations = []
            for idx, s in enumerate(gen_sentences, 1):
                evaluations.append({
                    "index": idx,
                    "sentence": s,
                    "verdict": "uncertain",
                    "explanation": "No reference provided for comparison.",
                    "corrected_sentence": None,
                    "confidence": 0.0
                })
            result["evaluations"] = evaluations
            return result

        prompt_sentences = "\n".join(
            [f"{i+1}. {s}" for i, s in enumerate(gen_sentences)])
        system_msg = (
            "You are a precise fact-checking assistant. Compare each generated sentence "
            "to the provided reference article. For every sentence, return a JSON object "
            "with fields: index (int), verdict ('correct' | 'incorrect' | 'uncertain'), "
            "explanation (short, objective), corrected_sentence (string or null if correct/uncertain), "
            "confidence (0.0-1.0). Only judge factual correctness relative to the reference content."
        )
        user_msg = (
            "Reference article:\n"
            f"{ref_clean}\n\n"
            "Generated article sentences:\n"
            f"{prompt_sentences}\n\n"
            "Return a JSON object with a 'evaluations' array containing one item per sentence, "
            "in the exact order. Example:\n"
            "{ \"evaluations\": [ { \"index\": 1, \"verdict\": \"correct\", \"explanation\": \"...\", "
            "\"corrected_sentence\": null, \"confidence\": 0.92 } ] }"
        )

        parsed = None
        if self._client is not None:
            try:
                # Try forcing JSON if supported
                completion = self._client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": user_msg}
                    ],
                    temperature=temperature,
                    # may raise if unsupported; caught below
                    response_format={"type": "json_object"}
                )
                content = completion.choices[0].message.content if completion and completion.choices else None
                result["raw_response"] = content
                parsed = self._safe_json_loads(content)
            except Exception:
                # Fallback without response_format
                try:
                    completion = self._client.chat.completions.create(
                        model=self.model,
                        messages=[
                            {"role": "system", "content": system_msg},
                            {"role": "user", "content": user_msg}
                        ],
                        temperature=temperature
                    )
                    content = completion.choices[0].message.content if completion and completion.choices else None
                    result["raw_response"] = content
                    parsed = self._safe_json_loads(content)
                except Exception as e2:
                    result["error"] = f"OpenAI API error: {e2}"

        if parsed and isinstance(parsed, dict) and "evaluations" in parsed:
            evaluations = self._normalize_evaluations(
                parsed.get("evaluations"), gen_sentences)
            result["evaluations"] = evaluations
            return result

        if result.get("error"):
            # API error already recorded; produce heuristic fallback
            result["evaluations"] = self._heuristic_compare(
                gen_sentences, ref_clean)
            return result

        # No API client available or parsing failed; fallback
        if self._client is None and result.get("error") is None:
            result["error"] = "OpenAI client not initialized. Using heuristic fallback."
        result["evaluations"] = self._heuristic_compare(
            gen_sentences, ref_clean)
        return result

    def calculate_accuracy_score(self, evaluation_data: Dict) -> float:
        '''
        Calculate a normalized accuracy score from evaluation data.
        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy
        Returns:
            A score between -1 and 1 for compatibility with existing scoring
        '''
        evals = evaluation_data.get("evaluations", []) if isinstance(
            evaluation_data, dict) else []
        correct = sum(1 for e in evals if self._verdict_of(e) == "correct")
        incorrect = sum(1 for e in evals if self._verdict_of(e) == "incorrect")
        evaluable = correct + incorrect
        if evaluable == 0:
            return 0.0
        score = (correct - incorrect) / float(evaluable)
        return max(-1.0, min(1.0, score))

    def calculate_accuracy_statistics(self, evaluation_data: Dict) -> Dict:
        '''
        Calculate statistics from the evaluation data.
        Args:
            evaluation_data: The line-by-line evaluation dictionary
        Returns:
            Dictionary with accuracy statistics
        '''
        evals = evaluation_data.get("evaluations", []) if isinstance(
            evaluation_data, dict) else []
        total = len(evals)
        correct = sum(1 for e in evals if self._verdict_of(e) == "correct")
        incorrect = sum(1 for e in evals if self._verdict_of(e) == "incorrect")
        uncertain = sum(1 for e in evals if self._verdict_of(e) == "uncertain")
        evaluable = correct + incorrect
        precision = (correct / evaluable) if evaluable else None
        score = self.calculate_accuracy_score(evaluation_data)
        return {
            "total_sentences": total,
            "correct": correct,
            "incorrect": incorrect,
            "uncertain": uncertain,
            "evaluable": evaluable,
            "precision": precision,
            "score": score
        }

    def evaluation_to_dataframe(self, evaluation_data: Dict) -> pd.DataFrame:
        '''
        Convert evaluation data to a pandas DataFrame for easier analysis.
        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy
        Returns:
            DataFrame with evaluation results
        '''
        evals = evaluation_data.get("evaluations", []) if isinstance(
            evaluation_data, dict) else []
        rows = []
        for e in evals:
            rows.append({
                "index": e.get("index"),
                "sentence": e.get("sentence"),
                "verdict": self._verdict_of(e),
                "explanation": e.get("explanation"),
                "corrected_sentence": e.get("corrected_sentence"),
                "confidence": e.get("confidence")
            })
        df = pd.DataFrame(rows, columns=[
                          "index", "sentence", "verdict", "explanation", "corrected_sentence", "confidence"])
        return df

    # Helpers

    def _clean_text(self, text: str) -> str:
        text = text or ""
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()

    def _split_into_sentences(self, text: str) -> List[str]:
        if not text:
            return []
        # Simple sentence segmentation
        # Protect common abbreviations from splitting
        protected = r"(Mr|Mrs|Ms|Dr|Prof|Sr|Jr|St|vs|etc|e\.g|i\.e|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
        pattern = re.compile(
            rf"(?<!{protected})\.(?=\s+[A-Z0-9\"'])|[!?](?=\s+|$)")
        indices = [0]
        sentences = []
        last = 0
        for m in pattern.finditer(text):
            end = m.end()
            segment = text[last:end].strip()
            if segment:
                sentences.append(segment)
            last = end
        tail = text[last:].strip()
        if tail:
            sentences.append(tail)
        # Further split very long lines on newlines if needed
        exploded: List[str] = []
        for s in sentences:
            parts = [p.strip() for p in re.split(r'\n+', s) if p.strip()]
            exploded.extend(parts)
        # Filter duplicates and trivial
        cleaned = []
        for s in exploded:
            s2 = s.strip()
            if len(s2) >= 2:
                cleaned.append(s2)
        return cleaned

    def _safe_json_loads(self, content: Optional[str]) -> Optional[Dict[str, Any]]:
        if not content or not isinstance(content, str):
            return None
        # Extract JSON block if surrounded by text
        candidate = content.strip()
        # Try to find the first JSON object
        start = candidate.find("{")
        end = candidate.rfind("}")
        if start != -1 and end != -1 and end > start:
            candidate = candidate[start:end+1]
        try:
            return json.loads(candidate)
        except Exception:
            return None

    def _normalize_evaluations(self, evaluations: Any, sentences: List[str]) -> List[Dict[str, Any]]:
        norm = []
        if not isinstance(evaluations, list):
            return self._pair_sentences_with_default(sentences)
        for i, s in enumerate(sentences, 1):
            # Try to find matching index
            item = None
            for ev in evaluations:
                idx = ev.get("index") if isinstance(ev, dict) else None
                if idx == i:
                    item = ev
                    break
            if not isinstance(item, dict):
                norm.append({
                    "index": i,
                    "sentence": s,
                    "verdict": "uncertain",
                    "explanation": "No evaluation returned for this sentence.",
                    "corrected_sentence": None,
                    "confidence": 0.0
                })
                continue
            verdict = str(item.get("verdict", "uncertain")).strip().lower()
            if verdict not in ("correct", "incorrect", "uncertain"):
                verdict = "uncertain"
            explanation = item.get("explanation")
            corrected = item.get("corrected_sentence")
            confidence = item.get("confidence")
            try:
                confidence = float(confidence)
            except Exception:
                confidence = None
            norm.append({
                "index": i,
                "sentence": s,
                "verdict": verdict,
                "explanation": explanation,
                "corrected_sentence": corrected if verdict == "incorrect" else None,
                "confidence": confidence
            })
        return norm

    def _pair_sentences_with_default(self, sentences: List[str]) -> List[Dict[str, Any]]:
        return [{
            "index": i + 1,
            "sentence": s,
            "verdict": "uncertain",
            "explanation": "No structured evaluation available.",
            "corrected_sentence": None,
            "confidence": 0.0
        } for i, s in enumerate(sentences)]

    def _heuristic_compare(self, gen_sentences: List[str], ref_text: str) -> List[Dict[str, Any]]:
        # Very basic heuristic: if most content words (after removing stop-like short words)
        # appear in reference, mark as likely correct; else uncertain/incorrect.
        ref_lower = ref_text.lower()
        evaluations: List[Dict[str, Any]] = []
        for idx, s in enumerate(gen_sentences, 1):
            words = re.findall(r"[A-Za-z0-9']+", s.lower())
            content_words = [w for w in words if len(w) >= 4]
            if not content_words:
                verdict = "uncertain"
                confidence = 0.2
            else:
                hits = sum(1 for w in content_words if w in ref_lower)
                ratio = hits / max(1, len(content_words))
                if ratio >= 0.7:
                    verdict = "correct"
                    confidence = min(1.0, 0.6 + 0.4 * ratio)
                elif ratio <= 0.3:
                    verdict = "incorrect"
                    confidence = min(1.0, 0.5 + 0.5 * (0.3 - ratio))
                else:
                    verdict = "uncertain"
                    confidence = 0.4
            evaluations.append({
                "index": idx,
                "sentence": s,
                "verdict": verdict,
                "explanation": "Heuristic evaluation based on lexical overlap with reference.",
                "corrected_sentence": None if verdict != "incorrect" else None,
                "confidence": confidence
            })
        return evaluations

    def _verdict_of(self, e: Dict[str, Any]) -> str:
        v = e.get("verdict")
        if isinstance(v, str):
            v = v.lower().strip()
            if v in ("correct", "incorrect", "uncertain"):
                return v
        return "uncertain"
