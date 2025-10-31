
import re
import difflib
from typing import Any, Dict, List, Set, Tuple, Union


class ReferenceValidator:
    _REF_PATTERN = re.compile(r'\$\{([^}]+)\}')

    @staticmethod
    def validate_step_references(workflow: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and correct step references in a workflow dictionary.

        The workflow is expected to contain a top‑level ``steps`` key whose value
        is a list of step dictionaries.  Each step dictionary may contain:

        * ``id`` – a unique identifier for the step.
        * ``parameters`` – a mapping of parameter names to values.  Values may
          contain references of the form ``${step_id.output_name}``.
        * ``request_body`` – a string or mapping that may also contain
          references of the same form.
        * ``outputs`` – a mapping of output names to values (used only for
          building the ``step_outputs`` mapping).

        The method will:

        1. Build a set of valid step identifiers.
        2. Build a mapping of step identifiers to their output dictionaries.
        3. Walk through each step and replace any invalid references with the
           best match (if one exists) or raise a ``ValueError``.
        4. Return the modified workflow dictionary.

        Parameters
        ----------
        workflow : dict
            The workflow dictionary to validate.

        Returns
        -------
        dict
            The workflow dictionary with references corrected.

        Raises
        ------
        ValueError
            If a reference cannot be resolved.
        """
        steps = workflow.get('steps', [])
        valid_step_ids: Set[str] = {
            step.get('id') for step in steps if 'id' in step}
        step_outputs: Dict[str, Any] = {
            step['id']: step.get('outputs', {})
            for step in steps
            if 'id' in step
        }

        ReferenceValidator._fix_parameter_references(
            workflow, valid_step_ids, step_outputs)
        ReferenceValidator._fix_request_body_references(
            workflow, valid_step_ids, step_outputs)

        return workflow

    @staticmethod
    def _find_best_match(target: str, candidates: List[str]) -> str | None:
        """
        Return the best candidate that matches ``target`` using a simple
        similarity metric.  The function uses ``difflib.get_close_matches`` to
        find the most similar candidate.  If no candidate is close enough
        (ratio < 0.6) ``None`` is returned.

        Parameters
        ----------
        target : str
            The string to match.
        candidates : list[str]
            Candidate strings to compare against.

        Returns
        -------
        str | None
            The best matching candidate or ``None`` if no suitable match is
            found.
        """
        matches = difflib.get_close_matches(
            target, candidates, n=1, cutoff=0.6)
        return matches[0] if matches else None

    @staticmethod
    def _fix_parameter_references(
        workflow: Dict[str, Any],
        valid_step_ids: Set[str],
        step_outputs: Dict[str, Any],
    ) -> None:
        """
        Walk through each step's ``parameters`` dictionary and replace any
        references that point to an unknown step id with the best match.

        Parameters
        ----------
        workflow : dict
            The workflow dictionary.
        valid_step_ids : set[str]
            Set of known step identifiers.
        step_outputs : dict[str, Any]
            Mapping of step identifiers to their output dictionaries.
        """
        for step in workflow.get('steps', []):
            params = step.get('parameters', {})
            if not isinstance(params, dict):
                continue
            for key, value in list(params.items()):
                if isinstance(value, str):
                    new_value = ReferenceValidator._replace_refs_in_string(
                        value, valid_step_ids, step_outputs
                    )
                    params[key] = new_value
                elif isinstance(value, list):
                    new_list = [
                        ReferenceValidator._replace_refs_in_string(
                            v, valid_step_ids, step_outputs)
                        if isinstance(v, str) else v
                        for v in value
                    ]
                    params[key] = new_list
                elif isinstance(value, dict):
                    # Recursively handle nested dicts
                    ReferenceValidator._fix_dict_refs(
                        value, valid_step_ids, step_outputs
                    )

    @staticmethod
    def _fix_request_body_references(
        workflow: Dict[str, Any],
        valid_step_ids: Set[str],
        step_outputs: Dict[str, Any],
    ) -> None:
        """
        Walk through each step's ``request_body`` field and replace any
        references that point to an unknown step id with the best match.

        Parameters
        ----------
        workflow : dict
            The workflow dictionary.
        valid_step_ids : set[str]
            Set of known step identifiers.
        step_outputs : dict[str, Any]
            Mapping of step identifiers to their output dictionaries.
        """
        for step in workflow.get('steps', []):
            body = step.get('request_body')
            if body is None:
                continue
            if isinstance(body, str):
                step['request_body'] = ReferenceValidator._replace_refs_in_string(
                    body, valid_step_ids, step_outputs
                )
            elif isinstance(body, dict):
                ReferenceValidator._fix_dict_refs(
                    body, valid_step_ids, step_outputs)
            elif isinstance(body, list):
                new_list = [
                    ReferenceValidator._replace_refs_in_string(
                        v, valid_step_ids, step_outputs)
                    if isinstance(v, str) else v
                    for v in body
                ]
                step['request_body'] = new_list

    @staticmethod
    def _replace_refs_in_string(
        text: str,
        valid_step_ids: Set[str],
        step_outputs: Dict[str, Any],
    ) -> str:
        """
        Replace all references in a string with corrected step ids if needed.

        Parameters
        ----------
        text : str
            The string containing potential references.
        valid_step_ids : set[str]
            Set of known step identifiers.
        step_outputs : dict[str, Any]
            Mapping of step identifiers to their output dictionaries.

        Returns
        -------
        str
            The string with references corrected.

        Raises
        ------
        ValueError
            If a reference cannot be resolved.
        """
        def repl(match: re.Match) -> str:
            ref = match.group(1).strip()
            if '.' not in ref:
                # malformed reference
                raise ValueError(f"Malformed reference: ${{{ref}}}")
            step_id, output_name = ref.split('.', 1)
            if step_id not in valid_step_ids:
                best = ReferenceValidator._find_best_match(
                    step_id, list(valid_step_ids))
                if best is None:
                    raise ValueError(f"Unknown step reference: {step_id}")
                step_id = best
            # Optionally validate that the output exists
            outputs = step_outputs.get(step_id, {})
            if output_name not in outputs:
                # We don't raise an error for missing output; just keep the reference
                pass
            return f"${{{step_id}.{output_name}}}"

        return ReferenceValidator._REF_PATTERN.sub(repl, text)

    @staticmethod
    def _fix_dict_refs(
        data: Dict[str, Any],
        valid_step_ids: Set[str],
        step_outputs: Dict[str, Any],
    ) -> None:
        """
        Recursively walk a dictionary and replace string references.

        Parameters
        ----------
        data : dict
            The dictionary to process.
        valid_step_ids : set[str]
            Set of known step identifiers.
        step_outputs : dict[str, Any]
            Mapping of step identifiers to their output dictionaries.
        """
        for k, v in list(data.items()):
            if isinstance(v, str):
                data[k] = ReferenceValidator._replace_refs_in_string(v,
