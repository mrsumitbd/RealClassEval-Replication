from typing import Any, Dict, Optional
from pathlib import Path
import argparse


class SearchAssistantConfig:
    """Configuration class for the Search Assistant."""

    def __init__(self, args: argparse.Namespace):
        """Initialize configuration from command line arguments.
        Args:
            args: Parsed command line arguments.
        """
        if isinstance(args, argparse.Namespace):
            data: Dict[str, Any] = vars(args).copy()
        elif isinstance(args, dict):
            data = dict(args)
        else:
            raise TypeError("args must be an argparse.Namespace or a dict")

        # Aliases to canonical names
        if "model" in data and "model_name" not in data:
            data["model_name"] = data["model"]
        if "index" in data and "index_path" not in data:
            data["index_path"] = data["index"]
        if "k" in data and "top_k" not in data:
            data["top_k"] = data["k"]
        if "temp" in data and "temperature" not in data:
            data["temperature"] = data["temp"]
        if "tokens" in data and "max_tokens" not in data:
            data["max_tokens"] = data["tokens"]

        # Defaults
        defaults: Dict[str, Any] = {
            "top_k": 5,
            "max_tokens": 256,
            "temperature": 0.2,
            "device": "cpu",
            "batch_size": 1,
            "timeout": 60,
        }
        for k, v in defaults.items():
            if data.get(k) is None:
                data[k] = v

        # Normalize device if present
        if "device" in data and isinstance(data["device"], str):
            data["device"] = data["device"].strip().lower()

        # Set as attributes
        for key, value in data.items():
            setattr(self, key, value)

        # Keep raw dictionary for reference
        self._data = data

    def validate(self) -> None:
        """Validate configuration parameters.
        Raises:
            ValueError: If any configuration parameter is invalid.
        """
        errors = []

        def coerce_int(name: str, minimum: Optional[int] = None, maximum: Optional[int] = None) -> Optional[int]:
            val = getattr(self, name, None)
            if val is None:
                return None
            try:
                intval = int(val)
            except (TypeError, ValueError):
                errors.append(f"{name} must be an integer, got {val!r}.")
                return None
            if minimum is not None and intval < minimum:
                errors.append(f"{name} must be >= {minimum}, got {intval}.")
            if maximum is not None and intval > maximum:
                errors.append(f"{name} must be <= {maximum}, got {intval}.")
            setattr(self, name, intval)
            return intval

        def coerce_float(name: str, minimum: Optional[float] = None, maximum: Optional[float] = None) -> Optional[float]:
            val = getattr(self, name, None)
            if val is None:
                return None
            try:
                fval = float(val)
            except (TypeError, ValueError):
                errors.append(f"{name} must be a float, got {val!r}.")
                return None
            if minimum is not None and fval < minimum:
                errors.append(f"{name} must be >= {minimum}, got {fval}.")
            if maximum is not None and fval > maximum:
                errors.append(f"{name} must be <= {maximum}, got {fval}.")
            setattr(self, name, fval)
            return fval

        # Validate numeric fields
        coerce_int("top_k", minimum=1)
        coerce_int("batch_size", minimum=1)
        coerce_int("max_tokens", minimum=1)
        coerce_int("embedding_dim", minimum=1)
        coerce_int("ef_search", minimum=1)
        coerce_int("nprobe", minimum=1)
        coerce_int("port", minimum=1, maximum=65535)
        coerce_int("timeout", minimum=1)

        # Validate floats
        coerce_float("temperature", minimum=0.0, maximum=2.0)
        coerce_float("top_p", minimum=0.0, maximum=1.0)

        # Validate device
        device = getattr(self, "device", None)
        if device is not None:
            if not isinstance(device, str):
                errors.append("device must be a string.")
            else:
                normalized = device.strip().lower()
                allowed_devices = {"cpu", "cuda", "gpu", "mps", "auto"}
                if normalized not in allowed_devices:
                    errors.append(
                        f"device must be one of {sorted(allowed_devices)}, got {device!r}.")
                else:
                    # Normalize some aliases
                    if normalized == "gpu":
                        normalized = "cuda"
                    setattr(self, "device", normalized)

        # Validate index path if provided
        index_path = getattr(self, "index_path", None)
        if index_path is not None:
            if isinstance(index_path, (str, Path)):
                p = Path(index_path)
                setattr(self, "index_path", p)
                if hasattr(self, "require_index_exists") and bool(getattr(self, "require_index_exists")):
                    if not p.exists():
                        errors.append(f"index_path does not exist: {p}")
            else:
                errors.append(
                    f"index_path must be a string or pathlib.Path, got {type(index_path).__name__}.")

        # Validate model name if provided
        model_name = getattr(self, "model_name", None)
        if model_name is not None and (not isinstance(model_name, str) or not model_name.strip()):
            errors.append("model_name must be a non-empty string if provided.")

        # Validate API key (if present)
        api_key = getattr(self, "api_key", None)
        if api_key is not None and (not isinstance(api_key, str) or not api_key.strip()):
            errors.append("api_key must be a non-empty string if provided.")

        # Validate retriever if provided
        retriever = getattr(self, "retriever", None)
        if retriever is not None:
            if not isinstance(retriever, str):
                errors.append("retriever must be a string if provided.")
            else:
                allowed_retrievers = {"bm25", "vector", "hybrid"}
                if retriever.lower() not in allowed_retrievers:
                    errors.append(
                        f"retriever must be one of {sorted(allowed_retrievers)}, got {retriever!r}.")

        # Validate similarity function if provided
        similarity_function = getattr(self, "similarity_function", None)
        if similarity_function is not None:
            if not isinstance(similarity_function, str):
                errors.append(
                    "similarity_function must be a string if provided.")
            else:
                allowed_sim = {"cosine", "dot", "l2"}
                if similarity_function.lower() not in allowed_sim:
                    errors.append(
                        f"similarity_function must be one of {sorted(allowed_sim)}, got {similarity_function!r}.")

        # Validate prompt_template if provided
        prompt_template = getattr(self, "prompt_template", None)
        if prompt_template is not None and not isinstance(prompt_template, str):
            errors.append("prompt_template must be a string if provided.")

        if errors:
            raise ValueError(
                "Invalid SearchAssistantConfig:\n- " + "\n- ".join(errors))
