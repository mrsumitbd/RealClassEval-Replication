
from typing import List, Dict, Any
import re
from collections import Counter


class NotesSearchController:

    def search_notes(self, notes: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        query_tokens = self._process_query(query)
        scored_notes = []

        for note in notes:
            title_tokens, content_tokens = self._process_note_content(note)
            score = self._calculate_score(
                query_tokens, title_tokens, content_tokens)
            scored_notes.append((note, score))

        scored_notes.sort(key=lambda x: x[1], reverse=True)
        return [note for note, score in scored_notes]

    def _process_query(self, query: str) -> List[str]:
        return self._tokenize_and_normalize(query)

    def _process_note_content(self, note: Dict[str, Any]) -> tuple[List[str], List[str]]:
        title_tokens = self._tokenize_and_normalize(note.get('title', ''))
        content_tokens = self._tokenize_and_normalize(note.get('content', ''))
        return title_tokens, content_tokens

    def _calculate_score(self, query_tokens: List[str], title_tokens: List[str], content_tokens: List[str]) -> float:
        title_counter = Counter(title_tokens)
        content_counter = Counter(content_tokens)
        query_counter = Counter(query_tokens)

        title_score = sum(
            query_counter[token] * title_counter[token] for token in query_counter)
        content_score = sum(
            query_counter[token] * content_counter[token] for token in query_counter)

        return title_score * 2 + content_score

    def _tokenize_and_normalize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b\w+\b', text)
        return tokens
