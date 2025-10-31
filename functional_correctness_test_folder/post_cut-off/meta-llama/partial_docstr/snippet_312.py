
from typing import List, Dict, Any
import re
from collections import Counter
import math


class NotesSearchController:

    def search_notes(self, notes: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        '''
        Search notes using token-based matching with relevance ranking.
        Returns notes sorted by relevance score.
        '''
        query_tokens = self._process_query(query)
        scored_notes = []
        for note in notes:
            title_tokens, content_tokens = self._process_note_content(note)
            score = self._calculate_score(
                query_tokens, title_tokens, content_tokens)
            scored_notes.append((note, score))
        scored_notes.sort(key=lambda x: x[1], reverse=True)
        return [note for note, score in scored_notes if score > 0]

    def _process_query(self, query: str) -> List[str]:
        query = re.sub(r'[^\w\s]', '', query).lower()
        return query.split()

    def _process_note_content(self, note: Dict[str, Any]) -> tuple[List[str], List[str]]:
        title = re.sub(r'[^\w\s]', '', note['title']).lower()
        content = re.sub(r'[^\w\s]', '', note.get('content', '')).lower()
        title_tokens = title.split()
        content_tokens = content.split()
        return title_tokens, content_tokens

    def _calculate_score(self, query_tokens: List[str], title_tokens: List[str], content_tokens: List[str]) -> float:
        query_token_counts = Counter(query_tokens)
        title_token_counts = Counter(title_tokens)
        content_token_counts = Counter(content_tokens)

        title_score = sum(min(
            query_token_counts[token], title_token_counts[token]) for token in query_token_counts)
        content_score = sum(min(
            query_token_counts[token], content_token_counts[token]) for token in query_token_counts)

        # Weighted scoring: title is more important than content
        score = title_score * 2 + content_score

        # Normalize score by the maximum possible score
        max_score = sum(query_token_counts.values()) * 2 + \
            sum(query_token_counts.values())
        if max_score > 0:
            score /= max_score

        # Apply a simple TF-IDF-like scoring by penalizing common query tokens
        for token in query_token_counts:
            if title_token_counts[token] + content_token_counts[token] > len(title_tokens) + len(content_tokens) / 2:
                score *= 0.5

        return score
