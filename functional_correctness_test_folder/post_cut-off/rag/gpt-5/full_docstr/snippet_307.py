from typing import Any, Optional
import difflib
import re
import copy


class ReferenceValidator:
    """Validates and fixes step references in Arazzo workflows."""

    # Common default output keys if explicit outputs are not provided
    _DEFAULT_OUTPUT_KEYS = {"body", "headers",
                            "status", "statusCode", "response", "data"}

    # Regex patterns to capture common reference syntaxes
    _REF_PATTERNS = [
        # Templating styles, e.g. {{ steps.stepA.outputs.body }}
        re.compile(
            r"\{\{\s*steps\.([A-Za-z0-9_\-]+)\.outputs\.([A-Za-z0-9_\-\.]+)\s*\}\}"),
        re.compile(
            r"\{\{\s*steps\.([A-Za-z0-9_\-]+)\.output[s]?\.([A-Za-z0-9_\-\.]+)\s*\}\}"),
        # JS/Handlebars-like ${steps.stepA.outputs.body}
        re.compile(
            r"\$\{\s*steps\.([A-Za-z0-9_\-]+)\.outputs\.([A-Za-z0-9_\-\.]+)\s*\}"),
        re.compile(
            r"\$\{\s*steps\.([A-Za-z0-9_\-]+)\.output[s]?\.([A-Za-z0-9_\-\.]+)\s*\}"),
        # URL-like: step://stepId/outputs/outputKey
        re.compile(r"step://([A-Za-z0-9_\-]+)/outputs?/([A-Za-z0-9_\-\.]+)"),
        # JSON pointer-like: #/steps/stepId/outputs/outputKey
        re.compile(r"#/steps/([A-Za-z0-9_\-]+)/outputs?/([A-Za-z0-9_\-\.]+)"),
    ]

    # Keys that may indicate a reference object with structured fields
    _STRUCTURED_REF_STEP_KEYS = ("step", "stepId", "fromStep", "sourceStep")
    _STRUCTURED_REF_OUTPUT_KEYS = (
        "output", "outputKey", "path", "key", "property")

    @staticmethod
    def validate_step_references(workflow: dict[str, Any]) -> dict[str, Any]:
        """Validate and fix step references in a workflow.
        This function checks all references to steps and their outputs in a workflow
        and fixes any inconsistencies.
        Args:
            workflow: The workflow to validate.
        Returns:
            The validated and fixed workflow.
        """
        if not isinstance(workflow, dict):
            return workflow

        steps = workflow.get("steps", [])
        if not isinstance(steps, list):
            return workflow

        # Build valid step IDs
        valid_step_ids: set[str] = set()
        for step in steps:
            if not isinstance(step, dict):
                continue
            step_id = step.get("id") or step.get("stepId") or step.get("name")
            if isinstance(step_id, str) and step_id:
                valid_step_ids.add(step_id)

        # Build step outputs map
        step_outputs: dict[str, set[str]] = {}
        for step in steps:
            if not isinstance(step, dict):
                continue
            step_id = step.get("id") or step.get("stepId") or step.get("name")
            if not isinstance(step_id, str) or not step_id:
                continue

            outputs_set: set[str] = set()

            # Explicit outputs
            outputs = step.get("outputs")
            if isinstance(outputs, dict):
                outputs_set.update(str(k) for k in outputs.keys())

            # Sometimes steps may define response-related structures
            responses = step.get("responses")
            if isinstance(responses, dict):
                outputs_set.update(str(k) for k in responses.keys())
                # Common nested outputs inside each response
                for resp in responses.values():
                    if isinstance(resp, dict):
                        outputs_set.update(
                            k for k in resp.keys() if isinstance(k, str))

            # Add defaults if nothing specific found to allow best-match behavior
            if not outputs_set:
                outputs_set = set(ReferenceValidator._DEFAULT_OUTPUT_KEYS)

            step_outputs[step_id] = outputs_set

        ReferenceValidator._fix_parameter_references(
            workflow, valid_step_ids, step_outputs)
        ReferenceValidator._fix_request_body_references(
            workflow, valid_step_ids, step_outputs)

        return workflow

    @staticmethod
    def _find_best_match(target: str, candidates: list[str]) -> str | None:
        """Find the best matching string from a list of candidates using sequence matching.
        Args:
            target: The target string to match.
            candidates: List of candidate strings.
        Returns:
            The best matching string or None if candidates is empty.
        """
        if not candidates:
            return None
        if target in candidates:
            return target
        # Try difflib with a reasonable cutoff
        matches = difflib.get_close_matches(
            target, candidates, n=1, cutoff=0.6)
        if matches:
            return matches[0]
        # Fallback manual ratio
        best: Optional[str] = None
        best_score = 0.0
        for c in candidates:
            score = difflib.SequenceMatcher(a=target, b=c).ratio()
            if score > best_score:
                best_score = score
                best = c
        return best

    @staticmethod
    def _fix_parameter_references(workflow: dict[str, Any], valid_step_ids: set[str], step_outputs: dict[str, Any]) -> None:
        """Fix parameter references in a workflow.
        Args:
            workflow: The workflow to fix.
            valid_step_ids: Set of valid step IDs.
            step_outputs: Dictionary mapping step IDs to their outputs.
        """
        steps = workflow.get("steps", [])
        if not isinstance(steps, list):
            return

        for step in steps:
            if not isinstance(step, dict):
                continue

            params = step.get("parameters")
            if params is None:
                continue

            fixed = ReferenceValidator._walk_and_fix(
                params, valid_step_ids, step_outputs)
            step["parameters"] = fixed

    @staticmethod
    def _fix_request_body_references(workflow: dict[str, Any], valid_step_ids: set[str], step_outputs: dict[str, Any]) -> None:
        """Fix request body references in a workflow.
        Args:
            workflow: The workflow to fix.
            valid_step_ids: Set of valid step IDs.
            step_outputs: Dictionary mapping step IDs to their outputs.
        """
        steps = workflow.get("steps", [])
        if not isinstance(steps, list):
            return

        for step in steps:
            if not isinstance(step, dict):
                continue

            rb = step.get("requestBody")
            if rb is None:
                continue

            fixed = ReferenceValidator._walk_and_fix(
                rb, valid_step_ids, step_outputs)
            step["requestBody"] = fixed

    @staticmethod
    def _walk_and_fix(value: Any, valid_step_ids: set[str], step_outputs: dict[str, set[str]]) -> Any:
        """Recursively walk a structure and fix references in strings and structured objects."""
        if isinstance(value, dict):
            # If dict looks like a structured reference, try to fix it
            if ReferenceValidator._looks_like_structured_reference(value):
                return ReferenceValidator._fix_structured_reference(copy.deepcopy(value), valid_step_ids, step_outputs)

            # Otherwise, recurse on members
            new_dict: dict[str, Any] = {}
            for k, v in value.items():
                new_dict[k] = ReferenceValidator._walk_and_fix(
                    v, valid_step_ids, step_outputs)
            return new_dict

        if isinstance(value, list):
            return [ReferenceValidator._walk_and_fix(v, valid_step_ids, step_outputs) for v in value]

        if isinstance(value, str):
            return ReferenceValidator._fix_string_reference(value, valid_step_ids, step_outputs)

        return value

    @staticmethod
    def _looks_like_structured_reference(obj: dict[str, Any]) -> bool:
        """Heuristic to detect if a dict is a structured reference."""
        has_step = any(
            k in obj for k in ReferenceValidator._STRUCTURED_REF_STEP_KEYS)
        has_output = any(
            k in obj for k in ReferenceValidator._STRUCTURED_REF_OUTPUT_KEYS)
        # Consider also objects that explicitly mark as reference
        is_marked_ref = "$ref" in obj or "ref" in obj or obj.get(
            "type") == "reference"
        return has_step or has_output or is_marked_ref

    @staticmethod
    def _fix_structured_reference(obj: dict[str, Any], valid_step_ids: set[str], step_outputs: dict[str, set[str]]) -> dict[str, Any]:
        """Fix a structured reference object."""
        # Normalize keys for step id
        step_key = next(
            (k for k in ReferenceValidator._STRUCTURED_REF_STEP_KEYS if k in obj), None)
        output_key = next(
            (k for k in ReferenceValidator._STRUCTURED_REF_OUTPUT_KEYS if k in obj), None)

        # Some references might encapsulate inside "$ref": "step://id/outputs/key"
        ref_str = obj.get("$ref") or obj.get("ref")
        if isinstance(ref_str, str):
            fixed = ReferenceValidator._fix_string_reference(
                ref_str, valid_step_ids, step_outputs)
            if fixed != ref_str:
                obj["$ref"] = fixed
                if "ref" in obj:
                    obj["ref"] = fixed

        if step_key:
            step_id_val = obj.get(step_key)
            if isinstance(step_id_val, str) and step_id_val:
                if step_id_val not in valid_step_ids:
                    best = ReferenceValidator._find_best_match(
                        step_id_val, list(valid_step_ids))
                    if best:
                        obj[step_key] = best

        if output_key:
            output_val = obj.get(output_key)
            # Determine the step to use for output matching
            step_id_for_output: Optional[str] = None
            if step_key and isinstance(obj.get(step_key), str):
                step_id_for_output = obj.get(step_key)
            # If no explicit step is present, try a generic best across all outputs
            if isinstance(output_val, str) and output_val:
                if step_id_for_output and step_id_for_output in step_outputs:
                    outputs = list(step_outputs.get(step_id_for_output, set()))
                    if output_val not in outputs:
                        best_output = ReferenceValidator._find_best_match(
                            output_val, outputs)
                        if best_output:
                            obj[output_key] = best_output
                else:
                    # Aggregate all possible outputs to find a reasonable best match
                    all_outputs = sorted(
                        {o for s in step_outputs.values() for o in s})
                    if output_val not in all_outputs:
                        best_output = ReferenceValidator._find_best_match(
                            output_val, all_outputs)
                        if best_output:
                            obj[output_key] = best_output

        # Recurse into nested structures in case there are embedded references
        for k, v in list(obj.items()):
            if isinstance(v, (dict, list)):
                obj[k] = ReferenceValidator._walk_and_fix(
                    v, valid_step_ids, step_outputs)

        return obj

    @staticmethod
    def _fix_string_reference(s: str, valid_step_ids: set[str], step_outputs: dict[str, set[str]]) -> str:
        """Fix references embedded in strings based on known patterns."""
        original = s

        def replace_match(m: re.Match) -> str:
            step_id = m.group(1)
            output_key = m.group(2)
            # Correct step id
            fixed_step = step_id if step_id in valid_step_ids else ReferenceValidator._find_best_match(
                step_id, list(valid_step_ids)) or step_id
            # Correct output key
            available_outputs = step_outputs.get(
                fixed_step, ReferenceValidator._DEFAULT_OUTPUT_KEYS)
            fixed_output = output_key if output_key in available_outputs else ReferenceValidator._find_best_match(
                output_key, list(available_outputs)) or output_key

            text = m.group(0)
            # Reconstruct based on the kind of pattern matched
            if text.startswith("{{"):
                # Keep same braces format
                return "{{ steps.%s.outputs.%s }}" % (fixed_step, fixed_output)
            if text.startswith("${"):
                return "${ steps.%s.outputs.%s }" % (fixed_step, fixed_output)
            if text.startswith("step://"):
                return "step://%s/outputs/%s" % (fixed_step, fixed_output)
            if text.startswith("#/steps/"):
                return "#/steps/%s/outputs/%s" % (fixed_step, fixed_output)
            # Fallback to original text if we cannot determine format
            return text

        # Apply each pattern iteratively
        new_s = s
        for pattern in ReferenceValidator._REF_PATTERNS:
            new_s = pattern.sub(replace_match, new_s)

        return new_s if new_s != original else s
