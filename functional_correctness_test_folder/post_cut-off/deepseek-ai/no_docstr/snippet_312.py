
from typing import List, Dict, Any
import re


class NotesSearchController:

    def search_notes(self, notes: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        if not query or not notes:
            return []

        query_tokens = self._process_query(query)
        scored_notes = []

        for note in notes:
            title_tokens, content_tokens = self._process_note_content(note)
            score = self._calculate_score(
                query_tokens, title_tokens, content_tokens)
            if score > 0:
                scored_notes.append((note, score))

        scored_notes.sort(key=lambda x: x[1], reverse=True)
        return [note for note, score in scored_notes]

    def _process_query(self, query: str) -> List[str]:
        query = query.lower()
        tokens = re.findall(r'\w+', query)
        return tokens

    def _process_note_content(self, note: Dict[str, Any]) -> tuple[List[str], List[str]]:
        title = note.get('title', '').lower()
        content = note.get('content', '').lower()

        title_tokens = re.findall(r'\w+', title)
        content_tokens = re.findall(r'\w+', content)

        return title_tokens, content_tokens

    def _calculate_score(self, query_tokens: List[str], title_tokens: List[str], content_tokens: List[str]) -> float:
        if not query_tokens:
            return 0.0

        title_score = 0.0
        content_score = 0.0

        for token in query_tokens:
            title_score += title_tokens.count(token) * 2.0
            content_score += content_tokens.count(token) * 1.0

        total_score = title_score + content_score
        return total_score
