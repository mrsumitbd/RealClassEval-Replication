from __future__ import annotations
import re
from typing import List, Dict, Any
from collections import Counter


class NotesSearchController:
    def search_notes(self, notes: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        '''
        Search notes using token-based matching with relevance ranking.
        Returns notes sorted by relevance score.
        '''
        query_tokens = self._process_query(query)
        if not query_tokens:
            return notes

        ranked = []
        for idx, note in enumerate(notes):
            title_tokens, content_tokens = self._process_note_content(note)
            score = self._calculate_score(
                query_tokens, title_tokens, content_tokens)
            if score > 0:
                ranked.append((score, idx, note))

        if not ranked:
            return []

        ranked.sort(key=lambda x: (-x[0], x[1]))
        return [n for _, _, n in ranked]

    def _process_query(self, query: str) -> List[str]:
        text = (query or "").lower()
        tokens = re.findall(r"\w+", text, flags=re.UNICODE)
        stopwords = {
            "the", "a", "an", "and", "or", "but", "if", "then", "else", "when", "at", "by",
            "for", "in", "of", "on", "to", "with", "without", "is", "are", "was", "were",
            "be", "been", "being", "as", "from", "that", "this", "these", "those", "it",
            "its", "into", "over", "under", "up", "down", "out", "about"
        }
        return [t for t in tokens if len(t) > 1 and t not in stopwords]

    def _process_note_content(self, note: Dict[str, Any]) -> tuple[List[str], List[str]]:
        '''
        Tokenize and normalize note title and content.
        '''
        title = str(note.get("title", "") or "").lower()
        content = str(note.get("content", "") or "").lower()
        title_tokens = re.findall(r"\w+", title, flags=re.UNICODE)
        content_tokens = re.findall(r"\w+", content, flags=re.UNICODE)
        return title_tokens, content_tokens

    def _calculate_score(self, query_tokens: List[str], title_tokens: List[str], content_tokens: List[str]) -> float:
        if not title_tokens and not content_tokens:
            return 0.0

        title_counts = Counter(title_tokens)
        content_counts = Counter(content_tokens)
        query_unique = list(dict.fromkeys(query_tokens)
                            )  # preserve order, unique

        score = 0.0

        # Frequency-weighted matches with title boost
        for qt in query_unique:
            t_cnt = title_counts.get(qt, 0)
            c_cnt = content_counts.get(qt, 0)
            if t_cnt or c_cnt:
                score += t_cnt * 3.0
                score += c_cnt * 1.0

        # Coverage bonuses
        matched_any = sum(
            1 for qt in query_unique if qt in title_counts or qt in content_counts)
        matched_title = sum(1 for qt in query_unique if qt in title_counts)

        if query_unique:
            coverage_ratio = matched_any / len(query_unique)
            title_coverage_ratio = matched_title / len(query_unique)
            score += coverage_ratio * 2.0
            score += title_coverage_ratio * 1.0

        # Phrase match bonus
        query_phrase = " ".join(query_tokens).strip()
        if query_phrase:
            title_text = " ".join(title_tokens)
            content_text = " ".join(content_tokens)
            if query_phrase and query_phrase in title_text:
                score += 5.0
            if query_phrase and query_phrase in content_text:
                score += 2.0

        # Light length normalization to avoid very long content dominating
        length_norm = (len(title_tokens) * 0.5 + len(content_tokens)) or 1
        score /= (1.0 + (length_norm / 500.0))

        return score
