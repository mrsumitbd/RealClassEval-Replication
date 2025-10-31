import random
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple, Union


class _SafeDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"


def _normalize_optional_pool(
    pool: Union[Mapping[str, str], Sequence[str]]
) -> List[Tuple[str, str]]:
    if isinstance(pool, Mapping):
        return [(str(k), str(v)) for k, v in pool.items()]
    else:
        return [(str(item), str(item)) for item in pool]


def _weighted_sample_without_replacement(
    items: List[Any], weights: Optional[Mapping[Any, float]], k: int
) -> List[Any]:
    if k <= 0 or not items:
        return []
    if k >= len(items):
        return list(items)

    remaining_items = list(items)
    if weights:
        remaining_weights = [float(weights.get(i, 1.0))
                             for i in remaining_items]
    else:
        remaining_weights = [1.0 for _ in remaining_items]

    chosen: List[Any] = []
    for _ in range(k):
        total = sum(w for w in remaining_weights if w > 0)
        if total <= 0:
            # fallback to uniform selection if weights are non-positive
            idx = random.randrange(len(remaining_items))
        else:
            r = random.uniform(0, total)
            acc = 0.0
            idx = 0
            for j, w in enumerate(remaining_weights):
                if w <= 0:
                    continue
                acc += w
                if r <= acc:
                    idx = j
                    break
        chosen.append(remaining_items.pop(idx))
        remaining_weights.pop(idx)
    return chosen


class templater:
    """Class for generating templates for question and answer generation.
    This class handles the creation of templates for generating both questions
    and answers based on predefined rules and configurations.
    """

    def __init__(
        self,
        q_dict: dict,
        a_dict: dict,
        user_name: str = "",
        global_bio: str = "",
        is_cot: bool = True,
    ):
        """Initialize the templater with question and answer dictionaries.
        Args:
            q_dict: Dictionary containing question type configurations.
            a_dict: Dictionary containing answer type configurations.
            user_name: Name of the user for personalization.
            global_bio: Global biography for context.
        """
        self.q_dict: Dict[str, Any] = dict(q_dict or {})
        self.a_dict: Dict[str, Any] = dict(a_dict or {})
        self.user_name = str(user_name or "").strip()
        self.global_bio = str(global_bio or "").strip()
        self.is_cot = bool(is_cot)

        self._default_q_base = (
            "You are generating a {question_type} question for {user_name}."
            " {global_bio}\n"
            "Follow the rules and produce only the question."
        ).strip()

        self._default_a_base = (
            "You are answering a {question_type} question for {user_name}."
            " {global_bio}\n"
            "{reasoning_instructions}\n"
            "Answer:"
        ).strip()

        self._default_cot = "First, think step by step and explain your reasoning before giving the final answer."
        self._default_no_cot = "Provide only the final answer without additional explanations."

    def _get_vars(self, extras: Optional[Mapping[str, Any]] = None) -> Mapping[str, Any]:
        vars_map = {
            "user_name": self.user_name,
            "global_bio": self.global_bio,
        }
        if extras:
            vars_map.update(extras)
        return _SafeDict(vars_map)

    def _compose_template(
        self, base: str, append: Optional[Iterable[str]] = None
    ) -> str:
        parts = [base.strip()]
        if append:
            for line in append:
                if line is None:
                    continue
                s = str(line).strip()
                if s:
                    parts.append(s)
        return "\n".join(parts).strip() + "\n"

    def _resolve_q_base(self, qtype: str) -> Tuple[str, List[str], Mapping[str, Any]]:
        config = self.q_dict.get(qtype)
        base = self.q_dict.get("base_template", self._default_q_base)
        append: List[str] = []
        vars_extra: Dict[str, Any] = {}

        if isinstance(config, str):
            base = config
        elif isinstance(config, Mapping):
            base = config.get("template", base)
            append = list(config.get("append", [])
                          ) if config.get("append") else []
            vars_extra = dict(config.get("variables", {}))

        return str(base), append, vars_extra

    def _resolve_a_base(self, qtype: str) -> Tuple[str, List[str], Mapping[str, Any], str]:
        config = self.a_dict.get(qtype)
        base = self.a_dict.get("base_template", self._default_a_base)
        append: List[str] = []
        vars_extra: Dict[str, Any] = {}
        cot_instruction = ""

        # Global defaults for CoT/no-CoT
        default_cot = self.a_dict.get("default_cot", self._default_cot)
        default_no_cot = self.a_dict.get(
            "default_no_cot", self._default_no_cot)

        if isinstance(config, str):
            base = config
        elif isinstance(config, Mapping):
            base = config.get("template", base)
            append = list(config.get("append", [])
                          ) if config.get("append") else []
            vars_extra = dict(config.get("variables", {}))
            if self.is_cot:
                cot_instruction = config.get("cot", default_cot)
            else:
                cot_instruction = config.get("no_cot", default_no_cot)
        else:
            cot_instruction = default_cot if self.is_cot else default_no_cot

        return str(base), append, vars_extra, str(cot_instruction)

    def _choose_optional(
        self, qtype: str
    ) -> Tuple[List[Tuple[str, str]], List[str]]:
        chosen_items: List[Tuple[str, str]] = []
        chosen_names: List[str] = []

        # Global optional
        global_optional = self.a_dict.get("optional")

        # Per-type optional overrides global
        per_type_config = self.a_dict.get(qtype)
        per_optional = None
        if isinstance(per_type_config, Mapping) and "optional" in per_type_config:
            per_optional = per_type_config.get("optional")

        optional_cfg = per_optional if per_optional is not None else global_optional

        if optional_cfg is None:
            return chosen_items, chosen_names

        pool: List[Tuple[str, str]] = []
        pick = 0
        weights_map: Optional[Dict[str, float]] = None
        require_names: List[str] = []

        if isinstance(optional_cfg, Mapping):
            raw_pool = optional_cfg.get("pool", {})
            pool = _normalize_optional_pool(
                raw_pool if raw_pool is not None else {})
            pick_raw = optional_cfg.get("pick", 0)
            if pick_raw == "all":
                pick = len(pool)
            else:
                try:
                    pick = int(pick_raw or 0)
                except Exception:
                    pick = 0
            weights_raw = optional_cfg.get("weights")
            if isinstance(weights_raw, Mapping):
                # ensure names match pool keys
                weights_map = {str(k): float(v)
                               for k, v in weights_raw.items()}
            require_raw = optional_cfg.get("require", [])
            require_names = [str(n) for n in require_raw] if isinstance(
                require_raw, Iterable) else []
        elif isinstance(optional_cfg, Sequence):
            pool = _normalize_optional_pool(optional_cfg)
            pick = len(pool)
        else:
            return chosen_items, chosen_names

        if not pool:
            return chosen_items, chosen_names

        pool_map = {name: text for name, text in pool}

        required = [(n, pool_map[n]) for n in require_names if n in pool_map]
        remaining_names = [n for n, _ in pool if n not in require_names]

        remaining_weights = {
            n: (weights_map.get(n, 1.0) if weights_map else 1.0) for n in remaining_names}
        to_pick = max(0, pick - len(required))
        selected_names = _weighted_sample_without_replacement(
            remaining_names, remaining_weights, to_pick)

        final_names = [n for n, _ in required] + selected_names
        final_items = [(n, pool_map[n]) for n in final_names]

        chosen_items = final_items
        chosen_names = final_names
        return chosen_items, chosen_names

    def get_A_template(self, question_type: str) -> tuple:
        """Generate the answer template for a specific question type.
        Args:
            question_type: The type of question to generate an answer for.
        Returns:
            A tuple containing the answer template and a list of chosen optional types.
        """
        qtype = str(question_type or "").strip() or "general"
        base, append, vars_extra, cot_instruction = self._resolve_a_base(qtype)
        optional_items, chosen_names = self._choose_optional(qtype)

        optional_texts = [text for _, text in optional_items]
        full = self._compose_template(base, append + optional_texts)

        variables = self._get_vars(
            {"question_type": qtype, "reasoning_instructions": cot_instruction, **vars_extra})
        template = full.format_map(variables)
        return template, chosen_names

    def get_Q_template(self, question_type_prompt: str) -> str:
        """Generate the question template based on the provided prompt.
        Args:
            question_type_prompt: The prompt describing the question type.
        Returns:
            The question generation template with the question type filled in.
        """
        qtype = str(question_type_prompt or "").strip() or "general"
        base, append, vars_extra = self._resolve_q_base(qtype)
        full = self._compose_template(base, append)
        variables = self._get_vars({"question_type": qtype, **vars_extra})
        return full.format_map(variables)
