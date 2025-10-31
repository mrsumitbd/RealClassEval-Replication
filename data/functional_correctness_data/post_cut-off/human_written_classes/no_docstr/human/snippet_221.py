class MMTokenAllocator:
    next_token_index: int

    def __init__(self):
        self.next_token_index = FIRST_MM_EMBEDDING_INDEX

    def allocate(self, num_tokens):
        idx = self.next_token_index
        self.next_token_index += num_tokens
        return idx