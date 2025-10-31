
class OutputMappingValidator:
    """Validates and fixes output mappings in Arazzo workflows."""

    @staticmethod
    def validate_output_mappings(workflow: dict[str, Any], openapi_spec: dict[str, Any], endpoints: dict[str, dict[str, Any]]) -> dict[str, Any]:
        """Validate and fix output mappings in a workflow.
        This function checks all output mappings in a workflow against the
        corresponding response schemas from the OpenAPI spec and fixes any
        inconsistencies.
        Args:
            workflow: The workflow to validate.
            openapi_spec: The OpenAPI specification.
            endpoints: Dictionary of endpoints from the OpenAPI parser.
        Returns:
            The validated and fixed workflow.
        """
        for step in workflow.get("steps", []):
            if "outputs" not in step:
                continue
            endpoint_data = OutputMappingValidator._get_endpoint_for_step(
                step, endpoints)
            if not endpoint_data:
                continue
            schema, headers = OutputMappingValidator._extract_response_info(
                endpoint_data)
            step["outputs"] = OutputMappingValidator._validate_step_outputs(
                step["outputs"], schema, headers)
        return workflow

    @staticmethod
    def _get_endpoint_for_step(step: dict[str, Any], endpoints: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
        """Get the endpoint data for a step.
        Args:
            step: The step to get the endpoint for.
            endpoints: Dictionary of endpoints from the OpenAPI parser.
        Returns:
            The endpoint data or None if not found.
        """
        step_name = step.get("name")
        if not step_name:
            return None
        return endpoints.get(step_name)

    @staticmethod
    def _extract_response_info(endpoint_data: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        """Extract response schema and headers from endpoint data.
        Args:
            endpoint_data: The endpoint data from the OpenAPI parser.
        Returns:
            A tuple of (response_schema, response_headers).
        """
        responses = endpoint_data.get("responses", {})
        success_response = responses.get("200", {}) or responses.get("201", {})
        schema = success_response.get("content", {}).get(
            "application/json", {}).get("schema", {})
        headers = success_response.get("headers", {})
        return schema, headers

    @staticmethod
    def _validate_step_outputs(outputs: dict[str, str], schema: dict[str, Any], headers: dict[str, Any]) -> dict[str, str]:
        """Validate and fix output mappings for a step.
        Args:
            outputs: The output mappings to validate.
            schema: The response schema.
            headers: The response headers.
        Returns:
            The validated and fixed output mappings.
        """
        validated_outputs = {}
        flat_schema = OutputMappingValidator._flatten_schema(
            schema.get("properties", {}))
        for output_name, output_path in outputs.items():
            normalized_path = OutputMappingValidator._normalize_property_path(
                output_path)
            if normalized_path in flat_schema:
                validated_outputs[output_name] = normalized_path
            else:
                best_match = OutputMappingValidator._find_best_property_match(
                    output_name, flat_schema)
                if best_match:
                    validated_outputs[output_name] = best_match
        return validated_outputs

    @staticmethod
    def _normalize_property_path(path: str) -> str:
        """Normalize a property path by removing array indices.
        Args:
            path: The property path to normalize.
        Returns:
            The normalized property path.
        """
        return path.replace("[0]", "").replace("[]", "")

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
        target_lower = target.lower()
        best_match = None
        best_score = -1
        for candidate in candidates:
            candidate_lower = candidate.lower()
            score = 0
            for i in range(min(len(target_lower), len(candidate_lower))):
                if target_lower[i] == candidate_lower[i]:
                    score += 1
                else:
                    break
            if score > best_score:
                best_score = score
                best_match = candidate
        return best_match

    @staticmethod
    def _find_best_property_match(output_name: str, flat_schema: dict[str, str]) -> str | None:
        """Find the best matching property in the schema for an output name.
        Args:
            output_name: The output name provided by the LLM.
            flat_schema: The flattened schema with property paths.
        Returns:
            The path to the matching property, or None if no match is found.
        """
        candidates = list(flat_schema.keys())
        return OutputMappingValidator._find_best_match(output_name, candidates)

    @staticmethod
    def _flatten_schema(properties: dict[str, Any], prefix: str = '') -> dict[str, str]:
        """Flatten a nested schema into a dictionary of property paths.
        Args:
            properties: The properties object from the schema.
            prefix: The prefix for nested properties.
        Returns:
            A dictionary mapping property names to their paths.
        """
        flat = {}
        for prop_name, prop_data in properties.items():
            current_path = f"{prefix}.{prop_name}" if prefix else prop_name
            if "properties" in prop_data:
                flat.update(OutputMappingValidator._flatten_schema(
                    prop_data["properties"], current_path))
            else:
                flat[prop_name] = current_path
        return flat
