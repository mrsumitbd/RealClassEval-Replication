from typing import List, Dict, Any
import re
import unicodedata
from collections import Counter


class NotesSearchController:
    '''Handles notes search logic and scoring.'''

    _STOPWORDS = {
        'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am',
        'an', 'and', 'any', 'are', 'as', 'at', 'be', 'because', 'been',
        'before', 'being', 'below', 'between', 'both', 'but', 'by',
        'could', 'did', 'do', 'does', 'doing', 'down', 'during', 'each',
        'few', 'for', 'from', 'further', 'had', 'has', 'have', 'having',
        'he', 'her', 'here', 'hers', 'herself', 'him', 'himself', 'his',
        'how', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'itself',
        'let', 'me', 'more', 'most', 'my', 'myself', 'no', 'nor', 'not',
        'of', 'off', 'on', 'once', 'only', 'or', 'other', 'our', 'ours',
        'ourselves', 'out', 'over', 'own', 'same', 'she', 'should', 'so',
        'some', 'such', 'than', 'that', 'the', 'their', 'theirs', 'them',
        'themselves', 'then', 'there', 'these', 'they', 'this', 'those',
        'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was',
        'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who',
        'whom', 'why', 'with', 'you', 'your', 'yours', 'yourself',
        'yourselves'
    }

    def search_notes(self, notes: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        '''
        Search notes using token-based matching with relevance ranking.
        Returns notes sorted by relevance score.
        '''
        query_tokens = self._process_query(query)
        if not query_tokens:
            return []

        ranked: List[tuple] = []
        for idx, note in enumerate(notes):
            title_tokens, content_tokens = self._process_note_content(note)
            score = self._calculate_score(
                query_tokens, title_tokens, content_tokens)
            if score > 0:
                ranked.append((score, idx, note))

        ranked.sort(key=lambda x: (-x[0], x[1]))
        return [n for _, _, n in ranked]

    def _process_query(self, query: str) -> List[str]:
        '''
        Tokenize and normalize the search query.
        '''
        return self._tokenize(query)

    def _process_note_content(self, note: Dict[str, Any]) -> tuple[List[str], List[str]]:
        '''
        Tokenize and normalize note title and content.
        '''
        title = note.get('title') or ''
        content = note.get('content') or ''
        return self._tokenize(title), self._tokenize(content)

    def _calculate_score(self, query_tokens: List[str], title_tokens: List[str], content_tokens: List[str]) -> float:
        '''
        Calculate a relevance score for a note based on query tokens.
        '''
        if not title_tokens and not content_tokens:
            return 0.0

        score = 0.0

        title_counter = Counter(title_tokens)
        content_counter = Counter(content_tokens)

        # preserve order, remove dups
        unique_query = list(dict.fromkeys(query_tokens))

        for qt in unique_query:
            title_exact = title_counter.get(qt, 0)
            content_exact = content_counter.get(qt, 0)

            # Exact token matches (title weighted higher)
            score += title_exact * 3.0
            score += content_exact * 1.5

            # Prefix (partial) matches for tokens length >= 3
            if len(qt) >= 3:
                title_prefix_count = sum(
                    count for tok, count in title_counter.items() if tok.startswith(qt))
                content_prefix_count = sum(
                    count for tok, count in content_counter.items() if tok.startswith(qt))

                # Avoid double-counting exacts
                title_prefix_count -= title_exact
                content_prefix_count -= content_exact

                if title_prefix_count > 0:
                    score += title_prefix_count * 1.2
                if content_prefix_count > 0:
                    score += content_prefix_count * 0.6

        # Full phrase bonus if the entire query sequence appears
        if len(query_tokens) >= 2:
            title_phrase_count = self._count_sequence(
                title_tokens, query_tokens)
            content_phrase_count = self._count_sequence(
                content_tokens, query_tokens)
            if title_phrase_count:
                score += title_phrase_count * 4.0
            if content_phrase_count:
                score += content_phrase_count * 2.0

            # Adjacent pair bonus (helps when full phrase isn't present)
            title_pair_hits = self._count_adjacent_pairs(
                title_tokens, query_tokens)
            content_pair_hits = self._count_adjacent_pairs(
                content_tokens, query_tokens)
            if title_pair_hits:
                score += title_pair_hits * 1.0
            if content_pair_hits:
                score += content_pair_hits * 0.5

        # If title starts with the query tokens, give a small boost
        if self._starts_with_sequence(title_tokens, query_tokens):
            score += 2.0

        return score

    # Helpers

    def _normalize(self, text: str) -> str:
        s = unicodedata.normalize('NFKD', str(text))
        s = s.encode('ascii', 'ignore').decode('ascii', 'ignore')
        return s.lower()

    def _tokenize(self, text: str) -> List[str]:
        normalized = self._normalize(text or '')
        tokens = re.findall(r'[a-z0-9]+', normalized)
        filtered: List[str] = []
        for t in tokens:
            if t in self._STOPWORDS:
                continue
            if len(t) < 2 and not t.isdigit():
                continue
            filtered.append(t)
        return filtered

    def _count_sequence(self, tokens: List[str], seq: List[str]) -> int:
        if not tokens or not seq or len(seq) > len(tokens):
            return 0
        count = 0
        n = len(seq)
        for i in range(len(tokens) - n + 1):
            if tokens[i:i + n] == seq:
                count += 1
        return count

    def _count_adjacent_pairs(self, tokens: List[str], seq: List[str]) -> int:
        if len(seq) < 2 or len(tokens) < 2:
            return 0
        pair_hits = 0
        seq_pairs = [(seq[i], seq[i + 1]) for i in range(len(seq) - 1)]
        token_pairs = [(tokens[i], tokens[i + 1])
                       for i in range(len(tokens) - 1)]
        token_pair_counter = Counter(token_pairs)
        for p in seq_pairs:
            pair_hits += token_pair_counter.get(p, 0)
        return pair_hits

    def _starts_with_sequence(self, tokens: List[str], seq: List[str]) -> bool:
        if not seq or not tokens or len(seq) > len(tokens):
            return False
        return tokens[:len(seq)] == seq
