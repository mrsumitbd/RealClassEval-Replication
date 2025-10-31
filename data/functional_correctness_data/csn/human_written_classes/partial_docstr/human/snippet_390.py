from gitlint.options import BoolOption, IntOption, ListOption, RegexOption, RuleOption, StrOption
import logging
from typing import ClassVar, Dict, List, Optional, Type
import copy
from dataclasses import dataclass, field

@dataclass
class Rule:
    """Class representing gitlint rules."""
    options_spec: ClassVar[List[RuleOption]] = []
    id: ClassVar[str]
    name: ClassVar[str]
    target: ClassVar[Optional[Type['LineRuleTarget']]] = None
    _log: ClassVar[Optional[logging.Logger]] = None
    _raw_options: Dict[str, str] = field(default_factory=dict, compare=False)
    options: Dict[str, RuleOption] = field(init=False)

    def __post_init__(self):
        self.options = {}
        for op_spec in self.options_spec:
            self.options[op_spec.name] = copy.deepcopy(op_spec)
            actual_option = self._raw_options.get(op_spec.name)
            if actual_option is not None:
                self.options[op_spec.name].set(actual_option)

    @property
    def log(self):
        if not self._log:
            self._log = logging.getLogger(__name__)
            logging.basicConfig()
        return self._log

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name and (self.options == other.options) and (self.target == other.target)

    def __str__(self):
        return f'{self.id} {self.name}'