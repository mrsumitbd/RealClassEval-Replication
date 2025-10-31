
from typing import List, Dict, Any, Tuple


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
        return query.lower().split()

    def _process_note_content(self, note: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        title_tokens = note.get('title', '').lower().split()
        content_tokens = note.get('content', '').lower().split()
        return title_tokens, content_tokens

    def _calculate_score(self, query_tokens: List[str], title_tokens: List[str], content_tokens: List[str]) -> float:
        title_score = sum(token in title_tokens for token in query_tokens)
        content_score = sum(token in content_tokens for token in query_tokens)
        return title_score * 2 + content_score
