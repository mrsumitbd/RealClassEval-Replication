
from __future__ import annotations

from typing import Any, Dict, List, Tuple, Optional


class OutputMappingValidator:
    @staticmethod
    def validate_output_mappings(
        workflow: dict[str, Any],
        openapi_spec: dict[str, Any],
        endpoints: dict[str, dict[str, Any]],
    ) -> dict[str, Any]:
        """
        Validate the output mappings defined in a workflow against the OpenAPI
        specification and the provided endpoints.

        Parameters
        ----------
        workflow : dict
            The workflow definition. Expected to contain a ``steps`` key with a
            list of step dictionaries. Each step may contain an ``outputs``
            mapping that maps output names to property paths.
        openapi_spec : dict
            The full OpenAPI specification.
        endpoints : dict
            A mapping from operationId to the corresponding endpoint data
            extracted from the OpenAPI spec.

        Returns
        -------
        dict
            A mapping from step name to a dictionary containing the validated
            outputs. The validated outputs dictionary maps each output name
            to the property path that was found in the schema or headers.
            If an output could not be validated, it is omitted from the
            dictionary.
        """
        validated: dict[str, Any] = {}
        for step in workflow.get("steps", []):
            step_name = step.get("name") or step.get(
                "id") or step.get("operationId")
            if not step_name:
                continue

            endpoint = OutputMappingValidator._get_endpoint_for_step(
                step, endpoints)
            if endpoint is None:
                continue

            schema, headers = OutputMappingValidator._extract_response_info(
                endpoint)
            if schema is None:
                continue

            outputs = step.get("outputs", {})
            if not isinstance(outputs, dict):
                continue

            validated_outputs = OutputMappingValidator._validate_step_outputs(
                outputs, schema, headers
            )
            if validated_outputs:
                validated[step_name] = {"outputs": validated_outputs}

        return validated

    @staticmethod
    def _get_endpoint_for_step(
        step: dict[str, Any], endpoints: dict[str, dict[str, Any]]
    ) -> Optional[dict[str, Any]]:
        """
        Find the endpoint data that corresponds to a workflow step.

        The step may specify an ``operationId`` or a ``name`` that matches an
        endpoint key. If no match is found, ``None`` is returned.
        """
        op_id = step.get("operationId") or step.get("name")
        if op_id and op_id in endpoints:
            return endpoints[op_id]
        return None

    @staticmethod
    def _extract_response_info(
        endpoint_data: dict[str, Any]
    ) -> Tuple[Optional[dict[str, Any]], Optional[dict[str, Any]]]:
        """
        Extract the response schema and headers from an endpoint definition.

        The function looks for the first 2xx response, then for the first
        media type under ``content``. If no schema or headers are found,
        ``None`` is returned for the respective value.
        """
        responses = endpoint_data.get("responses", {})
        # Find first 2xx response
        status_code = next(
            (code for code in responses if code.startswith("2")), None
        )
        if status_code is None:
            return None, None

        response = responses[status_code]
        headers = response.get("headers", {})

        content = response.get("content", {})
        if not content:
            return None, headers

        # Pick the first media type
        media_type = next(iter(content.values()))
        schema = media_type.get("schema")
        return schema, headers

    @staticmethod
    def _validate_step_outputs(
        outputs: dict[str, str], schema: dict[str, Any], headers: dict[str, Any]
    ) -> dict[str, str]:
        """
        Validate each output mapping against the provided schema and headers.

        For each output name, the function attempts to find a matching property
        path in the flattened schema or a header name. If a match is found,
        the mapping is kept; otherwise it is discarded.
        """
        flat_schema = OutputMappingValidator._flatten_schema(
            schema.get("properties", {}))
        validated: dict[str, str] = {}

        for output_name, prop_path in outputs.items():
            # Normalize the property path
            norm_path = OutputMappingValidator._normalize_property_path(
                prop_path)

            # Direct match in schema
            if norm_path in flat_schema:
                validated[output_name] = norm_path
                continue

            # Try best match in schema
            best_match = OutputMappingValidator._find_best_property_match(
                output_name, flat_schema
            )
            if best_match:
                validated[output_name] = best_match
                continue

            # Check headers
            if output_name in headers:
                validated[output_name] = output_name
                continue

            # Try best match in headers
            header_keys = list(headers.keys())
            best_header = OutputMappingValidator._find_best_match(
                output_name, header_keys)
            if best_header:
                validated[output_name] = best_header

        return validated

    @staticmethod
    def _normalize_property_path(path: str) -> str:
        """
        Normalise a property path by stripping leading/trailing slashes and
        collapsing multiple dots. This is a lightweight normalisation that
        keeps the path usable for matching against flattened schema keys.
        """
        return ".".join(part for part in path.strip("/").split(".") if part)

    @staticmethod
    def _find_best_match(target: str, candidates: List[str]) -> Optional[str]:
        """
        Find the best matching candidate for a target string.

        The function first checks for an exact match. If none is found, it
        calculates the Levenshtein distance to each candidate and returns
        the candidate with the smallest distance if that distance is
        less than or equal to 2. If no candidate meets the threshold,
        ``None`` is returned.
        """
        if target in candidates:
            return target

        def levenshtein(a: str, b: str) -> int:
            if len(a) < len(b):
                a, b = b, a
            previous_row = list(range(len(b) + 1))
            for i, ca in enumerate(a, 1):
                current_row = [i]
                for j, cb in enumerate(b, 1):
                    insertions = previous_row[j] + 1
                    deletions = current_row[j - 1] + 1
                    substitutions = previous_row[j - 1] + (ca != cb)
                    current_row.append(
                        min(insertions, deletions, substitutions))
                previous_row = current_row
            return previous_row[-1]

        best_candidate = None
        best_distance = None
        for cand in candidates:
            dist = levenshtein(target, cand)
            if best_distance is None or dist < best_distance:
                best_distance = dist
                best_candidate = cand

        if best_distance is not None and best_distance <= 2:
            return best_candidate
        return None

    @staticmethod
    def _find_best_property_match(
        output_name: str, flat_schema: Dict[str, str]
    ) -> Optional[str]:
        """
        Find the best matching property path in a flattened schema for a given
        output name. The function uses the same matching logic as
        ``_find_best_match`` but operates on the keys of the
