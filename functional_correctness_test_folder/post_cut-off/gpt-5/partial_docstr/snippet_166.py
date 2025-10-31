import argparse
from typing import Any, Iterable, Optional, Union


class SearchAssistantConfig:

    def __init__(self, args: argparse.Namespace):
        '''Initialize configuration from command line arguments.
        Args:
            args: Parsed command line arguments.
        '''
        if isinstance(args, argparse.Namespace):
            data = vars(args)
        elif isinstance(args, dict):
            data = dict(args)
        else:
            raise TypeError("args must be argparse.Namespace or dict")

        for k, v in data.items():
            setattr(self, k, v)

        # Normalize common fields if present
        self._coerce_if_present("top_k", int)
        self._coerce_if_present("page", int)
        self._coerce_if_present("limit", int)
        self._coerce_if_present("max_tokens", int)
        self._coerce_if_present("timeout", float)
        self._coerce_if_present("temperature", float)
        self._coerce_if_present("seed", int)

        self._normalize_bool_if_present("verbose")
        self._normalize_bool_if_present("debug")
        self._normalize_bool_if_present("stream")
        self._normalize_bool_if_present("use_cache")

        self._normalize_list_if_present("sources")
        self._normalize_list_if_present("filters")
        self._normalize_list_if_present("include")
        self._normalize_list_if_present("exclude")
        self._normalize_kv_list_if_present("metadata")

        self.validate()

    def _coerce_if_present(self, name: str, typ: Any) -> None:
        if hasattr(self, name):
            val = getattr(self, name)
            if val is None:
                return
            try:
                if typ is int:
                    setattr(self, name, int(val))
                elif typ is float:
                    setattr(self, name, float(val))
                elif typ is str:
                    setattr(self, name, str(val))
                else:
                    setattr(self, name, typ(val))  # type: ignore
            except (ValueError, TypeError):
                # Leave as-is; validate will catch
                pass

    def _normalize_bool_if_present(self, name: str) -> None:
        if hasattr(self, name):
            val = getattr(self, name)
            if isinstance(val, bool):
                return
            if isinstance(val, str):
                s = val.strip().lower()
                if s in {"1", "true", "yes", "y", "on"}:
                    setattr(self, name, True)
                elif s in {"0", "false", "no", "n", "off"}:
                    setattr(self, name, False)
            elif isinstance(val, (int, float)):
                setattr(self, name, bool(val))

    def _normalize_list_if_present(self, name: str) -> None:
        if hasattr(self, name):
            val = getattr(self, name)
            if val is None:
                return
            if isinstance(val, str):
                parts = [p.strip() for p in val.split(",") if p.strip()]
                setattr(self, name, parts)
            elif isinstance(val, Iterable) and not isinstance(val, (bytes, bytearray)):
                if isinstance(val, list):
                    return
                setattr(self, name, [v for v in val])

    def _normalize_kv_list_if_present(self, name: str) -> None:
        # Accept "k=v,k2=v2" or dict-like
        if hasattr(self, name):
            val = getattr(self, name)
            if val is None:
                return
            if isinstance(val, dict):
                return
            if isinstance(val, str):
                result = {}
                for item in [p for p in val.split(",") if p.strip()]:
                    if "=" in item:
                        k, v = item.split("=", 1)
                        result[k.strip()] = v.strip()
                setattr(self, name, result)

    def _in_range(self, value: Union[int, float], low: Optional[float] = None, high: Optional[float] = None, inclusive: bool = True) -> bool:
        if low is not None:
            if inclusive and value < low:
                return False
            if not inclusive and value <= low:
                return False
        if high is not None:
            if inclusive and value > high:
                return False
            if not inclusive and value >= high:
                return False
        return True

    def validate(self) -> None:
        errors = []

        # query: required non-empty string if present or if no alternative provided
        if hasattr(self, "query"):
            q = getattr(self, "query")
            if not isinstance(q, str) or not q.strip():
                errors.append("query must be a non-empty string")
        # Allow prompt as alternative
        elif hasattr(self, "prompt"):
            p = getattr(self, "prompt")
            if not isinstance(p, str) or not p.strip():
                errors.append("prompt must be a non-empty string")
        # If neither provided, it's optional depending on caller; do not error

        # top_k positive int if present
        if hasattr(self, "top_k"):
            tk = getattr(self, "top_k")
            if not isinstance(tk, int) or tk <= 0:
                errors.append("top_k must be a positive integer")

        # limit non-negative int if present
        if hasattr(self, "limit"):
            lim = getattr(self, "limit")
            if not isinstance(lim, int) or lim < 0:
                errors.append("limit must be a non-negative integer")

        # max_tokens positive int if present
        if hasattr(self, "max_tokens"):
            mt = getattr(self, "max_tokens")
            if not isinstance(mt, int) or mt <= 0:
                errors.append("max_tokens must be a positive integer")

        # temperature in [0,1] if present
        if hasattr(self, "temperature"):
            temp = getattr(self, "temperature")
            if not isinstance(temp, (int, float)) or not self._in_range(float(temp), 0.0, 1.0, inclusive=True):
                errors.append("temperature must be a number in [0, 1]")

        # timeout non-negative if present
        if hasattr(self, "timeout"):
            to = getattr(self, "timeout")
            if not isinstance(to, (int, float)) or float(to) < 0:
                errors.append("timeout must be a non-negative number")

        # sources list[str] if present
        if hasattr(self, "sources"):
            src = getattr(self, "sources")
            if not isinstance(src, list) or not all(isinstance(s, str) and s.strip() for s in src):
                errors.append("sources must be a list of non-empty strings")

        # filters list[str] if present
        if hasattr(self, "filters"):
            flt = getattr(self, "filters")
            if not isinstance(flt, list) or not all(isinstance(s, str) and s.strip() for s in flt):
                errors.append("filters must be a list of non-empty strings")

        # model non-empty string if present
        if hasattr(self, "model"):
            mdl = getattr(self, "model")
            if not isinstance(mdl, str) or not mdl.strip():
                errors.append("model must be a non-empty string")

        # endpoint non-empty string if present
        if hasattr(self, "endpoint"):
            ep = getattr(self, "endpoint")
            if not isinstance(ep, str) or not ep.strip():
                errors.append("endpoint must be a non-empty string")

        # api_key if present must be string (allow empty only if not required)
        if hasattr(self, "api_key"):
            ak = getattr(self, "api_key")
            if ak is not None and not isinstance(ak, str):
                errors.append("api_key must be a string")

        # stream boolean if present
        if hasattr(self, "stream") and not isinstance(getattr(self, "stream"), bool):
            errors.append("stream must be a boolean")

        # verbose boolean if present
        if hasattr(self, "verbose") and not isinstance(getattr(self, "verbose"), bool):
            errors.append("verbose must be a boolean")

        if errors:
            raise ValueError("Invalid configuration: " + "; ".join(errors))
