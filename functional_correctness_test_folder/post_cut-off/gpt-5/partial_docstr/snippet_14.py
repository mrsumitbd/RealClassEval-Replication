import random
import string
from typing import Dict, Any, List, Tuple, Optional


class templater:
    '''Class for generating templates for question and answer generation.
    This class handles the creation of templates for generating both questions
    and answers based on predefined rules and configurations.
        '''

    def __init__(self, q_dict: dict, a_dict: dict, user_name: str = '', global_bio: str = '', is_cot: bool = True):
        '''Initialize the templater with question and answer dictionaries.
        Args:
            q_dict: Dictionary containing question type configurations.
            a_dict: Dictionary containing answer type configurations.
            user_name: Name of the user for personalization.
            global_bio: Global biography for context.
        '''
        if not isinstance(q_dict, dict):
            raise TypeError("q_dict must be a dict")
        if not isinstance(a_dict, dict):
            raise TypeError("a_dict must be a dict")
        self.q_dict: Dict[str, Any] = q_dict
        self.a_dict: Dict[str, Any] = a_dict
        self.user_name: str = user_name or ''
        self.global_bio: str = global_bio or ''
        self.is_cot: bool = bool(is_cot)
        self._rng = random.Random()

        # Defaults
        self._default_q_template = (
            "You are a helpful assistant tasked with generating questions.\n"
            "Question type: {question_type}\n"
            "{bio_section}"
            "{user_section}"
            "Please produce a clear, concise question of this type."
        )
        self._default_a_template = (
            "Provide a helpful, accurate answer to the user's {question_type} question.\n"
            "{bio_section}"
            "{user_section}"
        )
        self._default_cot = "Think step by step, verify facts, and provide a final concise answer."

    def _safe_format(self, template: str, mapping: Dict[str, Any]) -> str:
        class SafeDict(dict):
            def __missing__(self, key):
                return "{" + key + "}"
        return string.Formatter().vformat(template, (), SafeDict(mapping))

    def _build_common_sections(self) -> Dict[str, str]:
        bio_section = f"Context bio: {self.global_bio}\n" if self.global_bio else ""
        user_section = f"User: {self.user_name}\n" if self.user_name else ""
        return {"bio_section": bio_section, "user_section": user_section}

    def _select_optional_items(self, optional_list: List[Dict[str, Any]], k: Optional[int]) -> List[Dict[str, Any]]:
        if not optional_list:
            return []
        # If k specified, use weighted selection without replacement
        if isinstance(k, int) and k > 0:
            pool = optional_list[:]
            weights = [float(item.get("weight", item.get("prob", 1.0)))
                       for item in pool]
            total = sum(w for w in weights if w > 0)
            if total <= 0:
                # if all weights non-positive, fall back to uniform
                weights = [1.0] * len(pool)
                total = float(len(pool))
            chosen = []
            # choose up to k without replacement
            for _ in range(min(k, len(pool))):
                # compute cumulative
                cum = []
                acc = 0.0
                for w in weights:
                    acc += max(w, 0.0)
                    cum.append(acc)
                if acc <= 0:
                    break
                r = self._rng.random() * acc
                idx = 0
                while idx < len(cum) and r > cum[idx]:
                    idx += 1
                chosen.append(pool.pop(idx))
                weights.pop(idx)
            return chosen
        # Otherwise include each with probability prob (default 0.5)
        chosen = []
        for item in optional_list:
            p = item.get("prob")
            if p is None:
                p = 0.5
            try:
                p = float(p)
            except Exception:
                p = 0.0
            if p <= 0:
                continue
            if p >= 1 or self._rng.random() < p:
                chosen.append(item)
        return chosen

    def get_A_template(self, question_type: str) -> tuple:
        '''Generate the answer template for a specific question type.
        Args:
            question_type: The type of question to generate an answer for.
        Returns:
            A tuple containing the answer template and a list of chosen optional types.
        '''
        if not isinstance(question_type, str) or not question_type:
            raise ValueError("question_type must be a non-empty string")

        cfg = self.a_dict.get(
            question_type) or self.a_dict.get("_default") or {}
        common = self._build_common_sections()

        base_tpl = cfg.get("template") or self._default_a_template
        cot_tpl = cfg.get("cot") if self.is_cot else ""
        if self.is_cot and not cot_tpl:
            cot_tpl = self._default_cot

        instructions = cfg.get("instructions")
        if isinstance(instructions, list):
            instr_text = "\n".join(
                str(x) for x in instructions if isinstance(x, (str, int, float)))
            if instr_text:
                instr_text = instr_text.rstrip() + "\n"
        elif isinstance(instructions, str):
            instr_text = instructions.rstrip() + "\n"
        else:
            instr_text = ""

        optional_list = cfg.get("optional") or cfg.get(
            "optional_sections") or []
        optional_k = cfg.get("optional_k")
        chosen_optionals = self._select_optional_items(optional_list if isinstance(
            optional_list, list) else [], optional_k if isinstance(optional_k, int) else None)

        optional_texts = []
        chosen_types = []
        for item in chosen_optionals:
            item_tpl = item.get("template") or item.get("text") or ""
            if not isinstance(item_tpl, str):
                continue
            item_mapping = {
                "question_type": question_type,
                "user_name": self.user_name,
                "global_bio": self.global_bio,
                **common,
            }
            optional_texts.append(self._safe_format(item_tpl, item_mapping))
            chosen_types.append(
                str(item.get("type") or item.get("name") or "optional"))

        mapping = {
            "question_type": question_type,
            "user_name": self.user_name,
            "global_bio": self.global_bio,
            **common,
        }

        parts = [
            self._safe_format(base_tpl, mapping).rstrip(),
        ]
        if cot_tpl:
            parts.append(self._safe_format(cot_tpl, mapping).rstrip())
        if instr_text:
            parts.append(self._safe_format(instr_text, mapping).rstrip())
        if optional_texts:
            parts.append("\n".join(s.rstrip()
                         for s in optional_texts if s).rstrip())

        final_template = "\n\n".join(p for p in parts if p) + "\n"
        return final_template, chosen_types

    def get_Q_template(self, question_type_prompt: str) -> str:
        '''Generate the question template based on the provided prompt.
        Args:
            question_type_prompt: The prompt describing the question type.
        Returns:
            The question generation template with the question type filled in.
        '''
        if not isinstance(question_type_prompt, str) or not question_type_prompt:
            raise ValueError("question_type_prompt must be a non-empty string")

        # Use a global q_dict structure; support either a single template or per-type dict
        qcfg = self.q_dict
        common = self._build_common_sections()

        # Attempt to select a per-type config if present, else use root
        per_type_cfg = None
        if "types" in qcfg and isinstance(qcfg["types"], dict):
            per_type_cfg = qcfg["types"].get(question_type_prompt)

        cfg = per_type_cfg or qcfg

        base_tpl = cfg.get("template") or cfg.get(
            "base_template") or self._default_q_template
        prefix = cfg.get("prefix", "")
        suffix = cfg.get("suffix", "")
        cot_q = cfg.get("cot_prompt") if self.is_cot else ""

        mapping = {
            "question_type": question_type_prompt,
            "user_name": self.user_name,
            "global_bio": self.global_bio,
            **common,
        }

        parts = []
        if isinstance(prefix, str) and prefix.strip():
            parts.append(self._safe_format(prefix, mapping).rstrip())
        parts.append(self._safe_format(base_tpl, mapping).rstrip())
        if isinstance(cot_q, str) and cot_q.strip():
            parts.append(self._safe_format(cot_q, mapping).rstrip())
        if isinstance(suffix, str) and suffix.strip():
            parts.append(self._safe_format(suffix, mapping).rstrip())

        return "\n\n".join(parts) + "\n"
