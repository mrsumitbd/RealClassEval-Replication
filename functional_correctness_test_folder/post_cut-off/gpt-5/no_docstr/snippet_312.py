from typing import List, Dict, Any, Tuple
import re
from collections import Counter


class NotesSearchController:
    def search_notes(self, notes: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        query_tokens = self._process_query(query)
        if not isinstance(notes, list):
            return []
        if not query_tokens:
            return [n.copy() for n in notes]

        results: List[Dict[str, Any]] = []
        for note in notes:
            title_tokens, content_tokens = self._process_note_content(note)
            score = self._calculate_score(
                query_tokens, title_tokens, content_tokens)
            if score > 0:
                note_copy = note.copy()
                note_copy["_score"] = score
                results.append(note_copy)

        results.sort(key=lambda x: x.get("_score", 0), reverse=True)
        return results

    def _process_query(self, query: str) -> List[str]:
        if not isinstance(query, str):
            return []
        tokens = re.findall(r"\b\w+\b", query.lower())
        # Deduplicate while preserving order
        seen = set()
        unique_tokens = []
        for t in tokens:
            if t and t not in seen:
                seen.add(t)
                unique_tokens.append(t)
        return unique_tokens

    def _process_note_content(self, note: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        title = str(note.get("title", "") if note is not None else "")
        content = str(note.get("content", "") if note is not None else "")
        title_tokens = re.findall(r"\b\w+\b", title.lower())
        content_tokens = re.findall(r"\b\w+\b", content.lower())
        return title_tokens, content_tokens

    def _calculate_score(self, query_tokens: List[str], title_tokens: List[str], content_tokens: List[str]) -> float:
        if not query_tokens:
            return 0.0

        title_counts = Counter(title_tokens)
        content_counts = Counter(content_tokens)

        # Base weights
        title_weight = 2.0
        content_weight = 1.0

        score = 0.0

        for qt in query_tokens:
            if qt in title_counts:
                score += title_counts[qt] * title_weight
            if qt in content_counts:
                score += content_counts[qt] * content_weight

        # Phrase/substring boosts
        title_text = " ".join(title_tokens)
        content_text = " ".join(content_tokens)
        if len(query_tokens) > 1:
            phrase = " ".join(query_tokens)
            if phrase and phrase in title_text:
                score += 2.0
            if phrase and phrase in content_text:
                score += 1.0

        # Coverage bonus: proportion of unique query terms found
        unique_query = set(query_tokens)
        found = sum(
            1 for t in unique_query if t in title_counts or t in content_counts)
        if unique_query:
            score += 0.5 * (found / len(unique_query))

        return score
