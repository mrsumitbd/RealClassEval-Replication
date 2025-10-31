
from __future__ import annotations

import re
from difflib import SequenceMatcher
from typing import Any, Dict, List, Tuple, Optional


class OutputMappingValidator:
    '''Validates and fixes output mappings in Arazzo workflows.'''

    @staticmethod
    def validate_output_mappings(
        workflow: dict[str, Any],
        openapi_spec: dict[str, Any],
        endpoints: dict[str, dict[str, Any]],
    ) -> dict[str, Any]:
        """Validate and fix output mappings in a workflow.

        This function checks all output mappings in a workflow against the
        corresponding response schemas from the OpenAPI spec and fixes any
        inconsistencies.
        """
        # Ensure we have a mutable copy
        wf = workflow.copy()
        steps = wf.get("steps", [])
        for step in steps:
            # Get endpoint data for this step
            endpoint_data = OutputMappingValidator._get_endpoint_for_step(
                step, endpoints)
            if not endpoint_data:
                continue

            # Extract response schema and headers
            schema, headers = OutputMappingValidator._extract_response_info(
                endpoint_data)

            # Validate and fix outputs
            outputs = step.get("outputs", {})
            if isinstance(outputs, dict):
                fixed_outputs = OutputMappingValidator._validate_step_outputs(
                    outputs, schema, headers
                )
                step["outputs"] = fixed_outputs

        return wf

    @staticmethod
    def _get_endpoint_for_step(
        step: dict[str, Any], endpoints: dict[str, dict[str, Any]]
    ) -> Optional[dict[str, Any]]:
        """Get the endpoint data for a step."""
        # Common identifiers: operationId, endpoint, path+method
        op_id = step.get("operationId") or step.get("endpoint")
        if op_id and op_id in endpoints:
            return endpoints[op_id]

        # Try path+method
        path = step.get("path")
        method = step.get("method", "").lower()
        if path and method:
            key = f"{method} {path}"
            return endpoints.get(key)

        return None

    @staticmethod
    def _extract_response_info(
        endpoint_data: dict[str, Any]
    ) -> Tuple[dict[str, Any], dict[str, Any]]:
        """Extract response schema and headers from endpoint data."""
        responses = endpoint_data.get("responses", {})
        # Prefer 2xx responses
        status_codes = sorted(responses.keys(), key=lambda s: int(
            s.split(" ")[0]) if s else 0)
        for code in status_codes:
            if code.startswith("2"):
                resp = responses[code]
                # Get JSON schema
                content = resp.get("content", {})
                json_schema = None
                for media_type in ("application/json", "application/*+json"):
                    if media_type in content:
                        json_schema = content[media_type].get("schema", {})
                        break
                if json_schema is None:
                    # Fallback: use the first content type
                    if content:
                        json_schema = next(
                            iter(content.values())).get("schema", {})
                headers = resp.get("headers", {})
                return json_schema or {}, headers or {}
        # If no 2xx, fallback to first response
        if responses:
            first_resp = next(iter(responses.values()))
            content = first_resp.get("content", {})
            json_schema = {}
            for media_type in ("application/json", "application/*+json"):
                if media_type in content:
                    json_schema = content[media_type].get("schema", {})
                    break
            if json_schema is None and content:
                json_schema = next(iter(content.values())).get("schema", {})
            headers = first_resp.get("headers", {})
            return json_schema or {}, headers or {}
        return {}, {}

    @staticmethod
    def _validate_step_outputs(
        outputs: dict[str, str], schema: dict[str, Any], headers: dict[str, Any]
    ) -> dict[str, str]:
        """Validate and fix output mappings for a step."""
        flat_schema = OutputMappingValidator._flatten_schema(
            schema.get("properties", {}))
        header_keys = {h.lower() for h in headers.keys()}
        fixed = {}
        for out_name, prop_path in outputs.items():
            # Normalize path
            norm_path = OutputMappingValidator._normalize_property_path(
                prop_path)
            # Check if path exists in schema
            if norm_path in flat_schema.values() or norm_path.lower() in header_keys:
                fixed[out_name] = prop_path
                continue
            # Try to find best match in schema properties
            best_match = OutputMappingValidator._find_best_property_match(
                out_name, flat_schema)
            if best_match:
                fixed[out_name] = best_match
            else:
                # Try header match
                best_header = OutputMappingValidator._find_best_match(
                    out_name, list(header_keys))
                if best_header:
                    fixed[out_name] = best_header
                else:
                    # Keep original if no match
                    fixed[out_name] = prop_path
        return fixed

    @staticmethod
    def _normalize_property_path(path: str) -> str:
        """Normalize a property path by removing array indices."""
        return re.sub(r"\[\d+\]", "", path)

    @staticmethod
    def _find_best_match(target: str, candidates: List[str]) -> Optional[str]:
        """Find the best matching string from a list of candidates using sequence matching."""
        if not candidates:
            return None
        best = None
        best_ratio = 0.0
        for cand in candidates:
            ratio = SequenceMatcher(None, target.lower(), cand.lower()).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best = cand
        # Threshold to avoid weak matches
        return best if best_ratio >= 0.6 else None

    @staticmethod
    def _find_best_property_match
