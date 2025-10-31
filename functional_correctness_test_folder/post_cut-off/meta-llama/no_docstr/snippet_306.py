
from typing import Any, Dict


class OutputMappingValidator:

    @staticmethod
    def validate_output_mappings(workflow: Dict[str, Any], openapi_spec: Dict[str, Any], endpoints: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validates output mappings in a workflow against an OpenAPI specification.

        Args:
        - workflow (Dict[str, Any]): The workflow to validate.
        - openapi_spec (Dict[str, Any]): The OpenAPI specification.
        - endpoints (Dict[str, Dict[str, Any]]): Endpoints from the OpenAPI specification.

        Returns:
        - Dict[str, Any]: A dictionary containing validation results.
        """
        validation_results = {}
        for step_name, step in workflow.get('steps', {}).items():
            endpoint = OutputMappingValidator._get_endpoint_for_step(
                step, endpoints)
            if endpoint:
                schema, headers = OutputMappingValidator._extract_response_info(
                    endpoint)
                outputs = step.get('outputs', {})
                validation_results[step_name] = OutputMappingValidator._validate_step_outputs(
                    outputs, schema, headers)
        return validation_results

    @staticmethod
    def _get_endpoint_for_step(step: Dict[str, Any], endpoints: Dict[str, Dict[str, Any]]) -> Dict[str, Any] | None:
        """
        Retrieves the endpoint associated with a given step.

        Args:
        - step (Dict[str, Any]): The step to find the endpoint for.
        - endpoints (Dict[str, Dict[str, Any]]): Endpoints from the OpenAPI specification.

        Returns:
        - Dict[str, Any] | None: The endpoint data if found, otherwise None.
        """
        endpoint_path = step.get('endpoint')
        if endpoint_path in endpoints:
            return endpoints[endpoint_path]
        return None

    @staticmethod
    def _extract_response_info(endpoint_data: Dict[str, Any]) -> tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Extracts response schema and headers from endpoint data.

        Args:
        - endpoint_data (Dict[str, Any]): Data for a specific endpoint.

        Returns:
        - tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response schema and headers.
        """
        responses = endpoint_data.get('responses', {})
        response_200 = responses.get('200', {})
        schema = response_200.get('content', {}).get(
            'application/json', {}).get('schema', {})
        headers = response_200.get('headers', {})
        return schema, headers

    @staticmethod
    def _validate_step_outputs(outputs: Dict[str, str], schema: Dict[str, Any], headers: Dict[str, Any]) -> Dict[str, str]:
        """
        Validates the outputs of a step against the response schema and headers.

        Args:
        - outputs (Dict[str, str]): Outputs defined in the step.
        - schema (Dict[str, Any]): The response schema.
        - headers (Dict[str, Any]): Response headers.

        Returns:
        - Dict[str, str]: A dictionary containing validation results for each output.
        """
        flat_schema = OutputMappingValidator._flatten_schema(
            schema.get('properties', {}))
        flat_headers = {OutputMappingValidator._normalize_property_path(
            key): key for key in headers.keys()}
        validation_results = {}
        for output_name, output_path in outputs.items():
            best_match = OutputMappingValidator._find_best_property_match(
                output_name, flat_schema)
            if best_match is None:
                best_match = OutputMappingValidator._find_best_match(
                    output_name, list(flat_headers.keys()))
                if best_match:
                    validation_results[output_name] = f'Mapped to header: {flat_headers[best_match]}'
                else:
                    validation_results[output_name] = 'No match found in schema or headers'
            else:
                validation_results[output_name] = f'Mapped to schema property: {best_match}'
        return validation_results

    @staticmethod
    def _normalize_property_path(path: str) -> str:
        """
        Normalizes a property path by removing any leading or trailing dots and converting to lower case.

        Args:
        - path (str): The property path to normalize.

        Returns:
        - str: The normalized property path.
        """
        return path.strip('.').lower()

    @staticmethod
    def _find_best_match(target: str, candidates: list[str]) -> str | None:
        """
        Finds the best match for a target string among a list of candidates.

        Args:
        - target (str): The target string to match.
        - candidates (list[str]): List of candidate strings.

        Returns:
        - str | None: The best match if found, otherwise None.
        """
        best_match = None
        best_ratio = 0
        for candidate in candidates:
            ratio = OutputMappingValidator._levenshtein_ratio(
                target.lower(), candidate.lower())
            if ratio > best_ratio:
                best_ratio = ratio
                best_match = candidate
        return best_match if best_ratio > 0.6 else None

    @staticmethod
    def _levenshtein_ratio(s1: str, s2: str) -> float:
        """
        Calculates the Levenshtein ratio between two strings.

        Args:
        - s1 (str): The first string.
        - s2 (str): The second string.

        Returns:
        - float: The Levenshtein ratio.
        """
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                cost = 0 if s1[i - 1] == s2[j - 1] else 1
                dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] +
                               1, dp[i - 1][j - 1] + cost)
        return 1 - dp[m][n] / max(m, n)

    @staticmethod
    def _find_best_property_match(output_name: str, flat_schema: Dict[str, str]) -> str | None:
        """
        Finds the best match for an output name in a flattened schema.

        Args:
        - output_name (str): The output name to match.
        - flat_schema (Dict[str, str]): The flattened schema.

        Returns:
        - str | None: The best match if found, otherwise None.
        """
        return OutputMappingValidator._find_best_match(output_name, list(flat_schema.keys()))

    @staticmethod
    def _flatten_schema(properties: Dict[str, Any], prefix: str = '') -> Dict[str, str]:
        """
        Flattens a nested schema into a dictionary of property paths.

        Args:
        - properties (Dict[str, Any]): The schema properties to flatten.
        - prefix (str): The prefix to use for property paths.

        Returns:
        - Dict[str, str]: A dictionary containing the flattened property paths.
        """
        flat_schema = {}
        for property_name, property_data in properties.items():
            property_path = f'{prefix}{property_name}' if prefix else property_name
            if 'properties' in property_data:
                flat_schema.update(OutputMappingValidator._flatten_schema(
                    property_data['properties'], property_path + '.'))
            else:
                flat_schema[OutputMappingValidator._normalize_property_path(
                    property_path)] = property_path
        return flat_schema
