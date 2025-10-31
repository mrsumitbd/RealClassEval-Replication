
from typing import List, Dict, Any, Tuple
import re


class NotesSearchController:
    """
    A simple token‑based search controller for notes.
    """

    def search_notes(self, notes: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        """
        Search notes using token‑based matching with relevance ranking.
        Returns notes sorted by relevance score (highest first).
        """
        if not query:
            return []

        query_tokens = self._process_query(query)
        scored_notes: List[Tuple[float, Dict[str, Any]]] = []

        for note in notes:
            title_tokens, content_tokens = self._process_note_content(note)
            score = self._calculate_score(
                query_tokens, title_tokens, content_tokens)
            if score > 0:
                scored_notes.append((score, note))

        # Sort by score descending
        scored_notes.sort(key=lambda x: x[0], reverse=True)
        return [note for _, note in scored_notes]

    def _process_query(self, query: str) -> List[str]:
        """
        Tokenize and normalize the search query.
        """
        # Lowercase and split on non‑alphanumeric characters
        tokens = re.findall(r"\b\w+\b", query.lower())
        return tokens

    def _process_note_content(self, note: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """
        Tokenize and normalize note title and content.
        """
        title = note.get("title", "")
        content = note.get("content", "")

        title_tokens = re.findall(r"\b\w+\b", title.lower())
        content_tokens = re.findall(r"\b\w+\b", content.lower())

        return title_tokens, content_tokens

    def _calculate_score(self, query_tokens: List[str], title_tokens: List[str], content_tokens: List[str]) -> float:
        """
        Calculate a relevance score based on token matches.
        Title matches are weighted higher than content matches.
        """
        title_set = set(title_tokens)
        content_set = set(content_tokens)

        score = 0.0
        for token in query_tokens:
            if token in title_set:
                score += 2.0  # title match weight
            elif token in content_set:
                score += 1.0  # content match weight

        return score
