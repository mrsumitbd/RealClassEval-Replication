import re

class SimpleTokenizer:
    """A basic model agnostic tokenizer."""

    def __init__(self, split_pattern='\\W+'):
        """Create a tokenizer based on a simple splitting pattern."""
        self.split_pattern = re.compile(split_pattern)

    def __call__(self, s, return_offsets_mapping=True):
        """Tokenize the passed string, optionally returning the offsets of each token in the original string."""
        pos = 0
        offset_ranges = []
        input_ids = []
        for m in re.finditer(self.split_pattern, s):
            start, end = m.span(0)
            offset_ranges.append((pos, start))
            input_ids.append(s[pos:start])
            pos = end
        if pos != len(s):
            offset_ranges.append((pos, len(s)))
            input_ids.append(s[pos:])
        out = {}
        out['input_ids'] = input_ids
        if return_offsets_mapping:
            out['offset_mapping'] = offset_ranges
        return out