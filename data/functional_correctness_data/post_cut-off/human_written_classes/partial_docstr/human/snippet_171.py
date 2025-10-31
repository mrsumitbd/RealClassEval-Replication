import spacy

class Chunker:

    def __init__(self, chunking_strategy: str='fixed', num_tokens: int=256, num_sentences: int=5) -> None:
        self.chunking_strategy = chunking_strategy
        assert chunking_strategy in ['fixed', 'sentences']
        self.nlp = spacy.load('en_core_web_sm')
        self.num_tokens = num_tokens
        self.num_sentences = num_sentences

    def count_tokens(self, document: str) -> int:
        return len(self.nlp(document))

    def chunk_by_sentences(self, document: str, num_sentences: int | None=None, overlap_sentences: int=1) -> tuple[list[str], list[tuple[int, int]]]:
        """
        Given a document (string), return the sentences as chunks and span annotations (start and end indices of chunks).
        Using spaCy to do sentence chunking.
        """
        if num_sentences is None:
            num_sentences = self.num_sentences
        if overlap_sentences >= num_sentences:
            print(f'Warning: overlap_sentences ({overlap_sentences}) is greater than num_sentences ({num_sentences}). Setting overlap to {num_sentences - 1}')
            overlap_sentences = num_sentences - 1
        doc = self.nlp(document)
        sentences = list(doc.sents)
        span_annotations = []
        chunks = []
        i = 0
        while i < len(sentences):
            chunk_sentences = sentences[i:i + num_sentences]
            if not chunk_sentences:
                break
            start_char = chunk_sentences[0].start_char
            end_char = chunk_sentences[-1].end_char
            chunks.append(document[start_char:end_char])
            span_annotations.append((start_char, end_char))
            i += num_sentences - overlap_sentences
        return (chunks, span_annotations)

    def chunk_by_tokens(self, document: str, num_tokens: int | None=None, overlap_tokens: int=32) -> tuple[list[str], list[tuple[int, int]]]:
        """
        Given a document (string), return the tokens as chunks and span annotations (start and end indices of chunks).
        Includes overlapping tokens between chunks for better context preservation.
        Uses spaCy for tokenization.
        """
        if num_tokens is None:
            num_tokens = self.num_tokens
        doc = self.nlp(document)
        tokens = list(doc)
        span_annotations = []
        chunks = []
        i = 0
        while i < len(tokens):
            end_idx = min(i + num_tokens, len(tokens))
            chunk_tokens = tokens[i:end_idx]
            start_char = chunk_tokens[0].idx
            end_char = chunk_tokens[-1].idx + len(chunk_tokens[-1])
            chunks.append(document[start_char:end_char])
            span_annotations.append((start_char, end_char))
            i += max(1, num_tokens - overlap_tokens)
        return (chunks, span_annotations)

    def chunk(self, document: str) -> tuple[list[str], list[tuple[int, int]]]:
        if self.chunking_strategy == 'sentences':
            return self.chunk_by_sentences(document)
        elif self.chunking_strategy == 'tokens':
            return self.chunk_by_tokens(document)
        else:
            raise ValueError(f'Invalid chunking strategy: {self.chunking_strategy}')