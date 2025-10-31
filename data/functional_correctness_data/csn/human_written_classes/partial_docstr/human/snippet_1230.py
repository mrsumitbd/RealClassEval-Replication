from typing import Any, List, Mapping, Optional, Tuple, Union
from bel.schemas.bel import AssertionStr, BelEntity, FunctionSpan, Key, NsArgSpan, NsVal, Pair, Span, ValidationError

class ParseInfo:
    """BEL Assertion Parse Information

    Matching quotes need to be gathered first
    """

    def __init__(self, assertion: AssertionStr=None, version: str='latest'):
        self.assertion = assertion
        self.version = version
        self.matched_quotes: List[Pair] = []
        self.matched_parens: List[Pair] = []
        self.commas: List[int] = []
        self.relations: List[Span] = []
        self.functions: List[FunctionSpan] = []
        self.nsargs: List[NsArgSpan]
        self.errors: List[ValidationError] = []
        if self.assertion:
            self.get_parse_info(assertion=self.assertion)

    def get_parse_info(self, assertion: str='', version: str='latest'):
        from bel.lang.parse import parse_info
        if assertion:
            self.assertion = assertion
        result = parse_info(self.assertion.entire, version=self.version)
        self.matched_quotes = result['matched_quotes']
        self.matched_parens = result['matched_parens']
        self.commas = result['commas']
        self.components = result['components']
        self.errors = result['errors']

    def __str__(self):
        components_str = ''
        for c in self.components:
            components_str += f'{str(c)}\n'
        return f'ParseInfo(\n            assertion: {self.assertion},\n            matched_quotes: {self.matched_quotes},\n            matched_parens: {self.matched_parens},\n            commas: {self.commas},\n            components: {components_str},\n            version: {self.version},\n            errors: {self.errors},\n        )\n        '
    __repr__ = __str__