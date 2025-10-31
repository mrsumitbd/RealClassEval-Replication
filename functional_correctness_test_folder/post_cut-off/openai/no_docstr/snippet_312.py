
import re
from typing import List, Dict, Any, Tuple


class NotesSearchController:
    """
    A simple search controller for notes. Each note is expected to be a dictionary
    containing at least the keys 'title' and 'content'.
    """

    def search_notes(self, notes: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        """
        Search the provided list of notes for the given query string.

        Parameters
        ----------
        notes : List[Dict[str, Any]]
            A list of note dictionaries. Each dictionary should contain at least
            the keys 'title' and 'content'.
        query : str
            The search query string.

        Returns
        -------
        List[Dict[str, Any]]
            The list of notes that match the query, sorted by relevance score
            (highest first). Notes with a score of 0 are omitted.
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

        # Return only the note dictionaries, preserving order
        return [note for _, note in scored_notes]

    def _process_query(self, query: str) -> List[str]:
        """
        Tokenise and normalise the query string.

        Parameters
        ----------
        query : str
            The raw query string.

        Returns
        -------
        List[str]
            A list of lower‑cased tokens extracted from the query.
        """
        # Split on non‑word characters, filter out empty strings, lower‑case
        tokens = re.split(r'\W+', query.lower())
        return [t for t in tokens if t]

    def _process_note_content(self, note: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """
        Extract and normalise the title and content tokens from a note.

        Parameters
        ----------
        note : Dict[str, Any]
            The note dictionary.

        Returns
        -------
        Tuple[List[str], List[str]]
            A tuple containing the list of title tokens and the list of content tokens.
        """
        title = note.get('title', '')
        content = note.get('content', '')

        title_tokens = re.split(r'\W+', title.lower())
        content_tokens = re.split(r'\W+', content.lower())

        title_tokens = [t for t in title_tokens if t]
        content_tokens = [t for t in content_tokens if t]

        return title_tokens, content_tokens

    def _calculate_score(self, query_tokens: List[str], title_tokens: List[str], content_tokens: List[str]) -> float:
        """
        Compute a relevance score for a note based on the query tokens.

        The scoring scheme is simple:
          * Each query token that appears in the title contributes 2 points.
          * Each query token that appears in the content contributes 1 point.

        Parameters
        ----------
        query_tokens : List[str]
            The list of tokens from the query.
        title_tokens : List[str]
            The list of tokens from the note's title.
        content_tokens : List[str]
            The list of tokens from the note's content.

        Returns
        -------
        float
            The computed relevance score.
        """
        score = 0.0
        title_set = set(title_tokens)
        content_set = set(content_tokens)

        for token in query_tokens:
            if token in title_set:
                score += 2.0
            if token in content_set:
                score += 1.0

        return score
