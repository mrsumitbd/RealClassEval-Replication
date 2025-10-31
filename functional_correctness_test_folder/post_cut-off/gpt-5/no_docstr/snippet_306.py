from __future__ import annotations

from typing import Any, Tuple, Optional, Dict, List
import difflib


class OutputMappingValidator:
    @staticmethod
    def validate_output_mappings(workflow: dict[str, Any], openapi_spec: dict[str, Any], endpoints: dict[str, dict[str, Any]]) -> dict[str, Any]:
        report: dict[str, Any] = {
            "steps": {},
            "summary": {"total_steps": 0, "steps_with_outputs": 0, "steps_with_issues": 0},
        }

        steps: list[dict[str, Any]] = workflow.get("steps", []) or []
        report["summary"]["total_steps"] = len(steps)

        for step in steps:
            step_id = str(step.get("id") or step.get("name") or step.get(
                "operationId") or step.get("endpoint") or "unknown")
            outputs: dict[str, str] = step.get("outputs") or {}
            if not isinstance(outputs, dict) or not outputs:
                report["steps"][step_id] = {
                    "valid": True,
                    "errors": [],
                    "suggestions": {},
                    "details": {"reason": "No outputs defined"},
                }
                continue

            report["summary"]["steps_with_outputs"] += 1

            endpoint_data = OutputMappingValidator._get_endpoint_for_step(
                step, endpoints)
            if not endpoint_data:
                report["steps"][step_id] = {
                    "valid": False,
                    "errors": ["Endpoint for step could not be resolved"],
                    "suggestions": {},
                    "details": {},
                }
                report["summary"]["steps_with_issues"] += 1
                continue

            schema, headers = OutputMappingValidator._extract_response_info(
                endpoint_data)
            suggestions = OutputMappingValidator._validate_step_outputs(
                outputs, schema, headers)

            valid = len(suggestions) == 0
            if not valid:
                report["summary"]["steps_with_issues"] += 1

            report["steps"][step_id] = {
                "valid": valid,
                "errors": [] if valid else ["One or more output mappings do not match the response schema or headers"],
                "suggestions": suggestions,
                "details": {
                    "operationId": endpoint_data.get("operationId"),
                    "path": endpoint_data.get("path"),
                    "method": endpoint_data.get("method"),
                },
            }

        return report

    @staticmethod
    def _get_endpoint_for_step(step: dict[str, Any], endpoints: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
        if not endpoints:
            return None

        candidates: list[str] = []
        direct_keys = [
            step.get("endpoint"),
            step.get("operationId"),
            step.get("id"),
            step.get("name"),
        ]
        for key in direct_keys:
            if isinstance(key, str):
                candidates.append(key)

        req = step.get("request") or {}
        if isinstance(req, dict):
            maybe_op = req.get("operationId")
            if isinstance(maybe_op, str):
                candidates.append(maybe_op)

        for key in candidates:
            if key in endpoints:
                return endpoints[key]

        # Try to match by operationId within endpoint objects
        wanted = None
        for key in candidates:
            for ep in endpoints.values():
                if isinstance(ep, dict) and ep.get("operationId") == key:
                    return ep
                if isinstance(ep, dict) and ep.get("id") == key:
                    return ep
                if isinstance(ep, dict) and ep.get("name") == key:
                    return ep
                if isinstance(ep, dict) and ep.get("path") == key:
                    wanted = ep

        return wanted

    @staticmethod
    def _extract_response_info(endpoint_data: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        responses = endpoint_data.get("responses") or {}
        if not isinstance(responses, dict):
            return {}, {}

        # Prefer 200, 201, 2xx, default
        preferred_keys = []
        for code in ("200", "201", "202", "204"):
            if code in responses:
                preferred_keys.append(code)
        # Add any other 2xx
        preferred_keys.extend([k for k in responses.keys() if str(
            k).isdigit() and str(k).startswith("2") and k not in preferred_keys])
        if "default" in responses:
            preferred_keys.append("default")
        # Fallback: any available key
        if not preferred_keys and responses:
            preferred_keys.extend(list(responses.keys()))

        schema: dict[str, Any] = {}
        headers: dict[str, Any] = {}

        for key in preferred_keys:
            resp = responses.get(key) or {}
            if not isinstance(resp, dict):
                continue
            headers = resp.get("headers") or {}
            content = resp.get("content") or {}
            if isinstance(content, dict):
                # Prefer JSON
                json_media = None
                for mt in ("application/json", "application/*+json"):
                    if mt in content:
                        json_media = content[mt]
                        break
                # Fallback to any media with schema
                if not json_media:
                    for mt_data in content.values():
                        if isinstance(mt_data, dict) and "schema" in mt_data:
                            json_media = mt_data
                            break
                if isinstance(json_media, dict):
                    maybe_schema = json_media.get("schema")
                    if isinstance(maybe_schema, dict):
                        schema = maybe_schema
                        break

            # If no content, see if response directly has schema (non-standard)
            maybe_schema = resp.get("schema")
            if isinstance(maybe_schema, dict):
                schema = maybe_schema
                break

        return schema or {}, headers or {}

    @staticmethod
    def _validate_step_outputs(outputs: dict[str, str], schema: dict[str, Any], headers: dict[str, Any]) -> dict[str, str]:
        suggestions: dict[str, str] = {}

        # Flatten schema for property path checks
        flat_schema: dict[str, str] = {}
        if isinstance(schema, dict):
            if schema.get("type") == "array" and isinstance(schema.get("items"), dict):
                items = schema["items"]
                if items.get("type") == "object" and isinstance(items.get("properties"), dict):
                    flat_schema = OutputMappingValidator._flatten_schema(
                        items.get("properties") or {}, prefix="[]")
                else:
                    flat_schema = {"[]": items.get("type", "any")}
            elif schema.get("type") == "object" and isinstance(schema.get("properties"), dict):
                flat_schema = OutputMappingValidator._flatten_schema(
                    schema.get("properties") or {}, prefix="")
            elif "properties" in schema and isinstance(schema["properties"], dict):
                flat_schema = OutputMappingValidator._flatten_schema(
                    schema["properties"], prefix="")
            else:
                flat_schema = {}

        header_names = set(h.lower() for h in headers.keys()
                           ) if isinstance(headers, dict) else set()

        # Validate each output mapping
        for out_name, target in outputs.items():
            if not isinstance(target, str) or not target.strip():
                suggestions[out_name] = ""
                continue

            normalized = OutputMappingValidator._normalize_property_path(
                target)

            # Handle special tokens
            if normalized in ("status", "status_code"):
                continue  # assume always valid

            if normalized.startswith("headers."):
                hdr = normalized[len("headers."):].strip()
                if hdr.lower() in header_names:
                    continue
                # suggest closest header
                best = OutputMappingValidator._find_best_match(
                    hdr.lower(), list(header_names))
                if best:
                    suggestions[out_name] = f"headers.{best}"
                else:
                    suggestions[out_name] = ""
                continue

            # Assume body.* or plain property paths mean body
            prop_path = normalized
            if prop_path.startswith("body."):
                prop_path = prop_path[len("body."):]

            # direct match
            if prop_path in flat_schema:
                continue

            # try slight variations
            alt_candidates = set()
            alt_candidates.add(prop_path.replace("[]", "").strip("."))
            alt_candidates.add(prop_path.replace(".", ".properties."))
            alt_candidates.add(prop_path.replace(".items.", "."))
            # Also allow root array prefix variations
            if prop_path.startswith("[]"):
                alt_candidates.add(prop_path[2:].lstrip("."))
            for cand in list(alt_candidates):
                if cand in flat_schema:
                    alt_candidates = {cand}
                    break

            if any(c in flat_schema for c in alt_candidates):
                continue

            best_prop = OutputMappingValidator._find_best_property_match(
                prop_path, flat_schema)
            if best_prop:
                suggestions[out_name] = f"body.{best_prop}"
            else:
                suggestions[out_name] = ""

        # prune empty suggestions
        suggestions = {k: v for k, v in suggestions.items() if v is not None}
        return suggestions

    @staticmethod
    def _normalize_property_path(path: str) -> str:
        s = (path or "").strip()
        # Drop common prefixes
        for prefix in ("$.", "$", "response.", "result."):
            if s.startswith(prefix):
                s = s[len(prefix):]
        s = s.strip()
        # Normalize spaces
        s = ".".join(part.strip() for part in s.split(".") if part.strip())
        # Keep case for the path but treat headers case-insensitively downstream
        return s

    @staticmethod
    def _find_best_match(target: str, candidates: list[str]) -> str | None:
        if not target or not candidates:
            return None
        matches = difflib.get_close_matches(
            target, candidates, n=1, cutoff=0.6)
        return matches[0] if matches else None

    @staticmethod
    def _find_best_property_match(output_name: str, flat_schema: dict[str, str]) -> str | None:
        candidates = list(flat_schema.keys())
        # Try exact ignoring [] markers
        normalized_target = output_name.replace("[]", "")
        exact = [c for c in candidates if c.replace(
            "[]", "") == normalized_target]
        if exact:
            return exact[0]
        # Fuzzy match by segments
        target = output_name
        best = OutputMappingValidator._find_best_match(target, candidates)
        if best:
            return best
        # Try with last segment
        last = target.split(".")[-1]
        best = OutputMappingValidator._find_best_match(
            last, [c.split(".")[-1] for c in candidates])
        if best:
            # map back to original candidate that endswith that segment
            for c in candidates:
                if c.split(".")[-1] == best:
                    return c
        return None

    @staticmethod
    def _flatten_schema(properties: dict[str, Any], prefix: str = "") -> dict[str, str]:
        flat: dict[str, str] = {}

        def walk(node: dict[str, Any], base: str):
            if not isinstance(node, dict):
                return
            props = node.get("properties") if "properties" in node else node
            if not isinstance(props, dict):
                return

            for name, prop in props.items():
                seg = name
                path = f"{base}.{seg}" if base else seg
                if not isinstance(prop, dict):
                    flat[path] = "any"
                    continue

                ptype = prop.get("type")
                if ptype == "object" or "properties" in prop:
                    flat[path] = "object"
                    walk(prop, path)
                elif ptype == "array":
                    items = prop.get("items") or {}
                    array_path = f"{path}[]"
                    if isinstance(items, dict):
                        itype = items.get("type")
                        if itype == "object" or "properties" in items:
                            flat[array_path] = "array<object>"
                            walk(items, array_path)
                        else:
                            flat[array_path] = f"array<{items.get('type','any')}>"
                    else:
                        flat[array_path] = "array<any>"
                else:
                    flat[path] = ptype or "any"

        # If prefix indicates root array
        if prefix.startswith("[]"):
            root_base = prefix
            walk({"properties": properties}, root_base)
        else:
            walk(properties, prefix.strip("."))

        return flat
