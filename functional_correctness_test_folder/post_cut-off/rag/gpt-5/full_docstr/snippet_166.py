from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Iterable, List, Optional, Union


class SearchAssistantConfig:
    """Configuration class for the Search Assistant."""

    def __init__(self, args: argparse.Namespace):
        """Initialize configuration from command line arguments.

        Args:
            args: Parsed command line arguments.
        """
        if not isinstance(args, argparse.Namespace):
            raise TypeError("args must be an argparse.Namespace")

        self._raw_args = vars(args).copy()

        # Core/commonly-used options
        self.model: Optional[str] = self._get(
            args, ["model", "model_name"], None)
        self.embedding_model: Optional[str] = self._get(
            args, ["embedding_model", "embed_model"], None)
        self.vector_store: str = str(
            self._get(args, ["vector_store", "store"], "faiss")).lower()

        # Paths
        self.index_path: Optional[Path] = self._path(
            self._get(args, ["index_path", "index", "index_file"], None))
        self.data_dir: Optional[Path] = self._path(self._get(
            args, ["data_dir", "documents", "corpus_dir", "docs"], None), is_dir=True)
        self.cache_dir: Optional[Path] = self._path(
            self._get(args, ["cache_dir", "cache"], None), is_dir=True)

        # Numeric parameters
        self.top_k: int = int(self._get(args, ["top_k", "k"], 5))
        self.max_results: int = int(
            self._get(args, ["max_results", "max", "n_results"], self.top_k))
        self.temperature: Optional[float] = self._maybe_float(
            self._get(args, ["temperature", "temp"], 0.0))
        self.max_tokens: Optional[int] = self._maybe_int(
            self._get(args, ["max_tokens", "tokens"], 512))
        self.timeout: Optional[float] = self._maybe_float(
            self._get(args, ["timeout"], 60.0))

        # Misc settings
        self.device: Optional[str] = self._lower_or_none(
            self._get(args, ["device"], None))
        self.log_level: str = str(
            self._get(args, ["log_level", "loglevel"], "INFO")).upper()
        self.verbose: bool = self._as_bool(self._get(args, ["verbose"], False))
        self.persist: bool = self._as_bool(self._get(args, ["persist"], True))
        if hasattr(args, "no_persist") and getattr(args, "no_persist"):
            self.persist = False
        self.create_missing: bool = self._as_bool(
            self._get(args, ["create_missing", "mkdir"], True))
        self.seed: Optional[int] = self._maybe_int(
            self._get(args, ["seed"], None))
        self.api_key: Optional[str] = self._get(args, ["api_key", "key"], None)
        self.suppress_warnings: bool = self._as_bool(
            self._get(args, ["suppress_warnings", "no_warn"], False))
        self.use_color: bool = not self._as_bool(
            self._get(args, ["no_color"], False))
        self.language: Optional[str] = self._lower_or_none(
            self._get(args, ["language", "lang"], None))
        self.user: Optional[str] = self._get(args, ["user", "username"], None)
        self.session: Optional[str] = self._get(
            args, ["session", "session_id"], None)

        # Patterns/filters
        self.include_patterns: Optional[List[str]] = self._as_list(
            self._get(args, ["include", "include_patterns"], None))
        self.exclude_patterns: Optional[List[str]] = self._as_list(
            self._get(args, ["exclude", "exclude_patterns"], None))

        # Validate and finalize
        self.validate()

    def validate(self) -> None:
        """Validate configuration parameters.

        Raises:
            ValueError: If any configuration parameter is invalid.
        """
        valid_log_levels = {"CRITICAL", "ERROR",
                            "WARNING", "INFO", "DEBUG", "NOTSET"}
        if self.log_level not in valid_log_levels:
            raise ValueError(
                f"log_level must be one of {sorted(valid_log_levels)}")

        if not isinstance(self.top_k, int) or self.top_k <= 0:
            raise ValueError("top_k must be a positive integer")

        if not isinstance(self.max_results, int) or self.max_results <= 0:
            raise ValueError("max_results must be a positive integer")

        if self.temperature is not None:
            try:
                t = float(self.temperature)
            except Exception as e:
                raise ValueError("temperature must be a float") from e
            if not (0.0 <= t <= 2.0):
                raise ValueError("temperature must be between 0.0 and 2.0")

        if self.max_tokens is not None:
            if not isinstance(self.max_tokens, int) or self.max_tokens <= 0:
                raise ValueError("max_tokens must be a positive integer")

        if self.timeout is not None:
            try:
                to = float(self.timeout)
            except Exception as e:
                raise ValueError(
                    "timeout must be a positive number (seconds)") from e
            if to <= 0:
                raise ValueError("timeout must be a positive number (seconds)")

        if self.device is not None:
            dev = self.device
            if not (dev == "cpu" or dev == "mps" or dev.startswith("cuda")):
                raise ValueError(
                    "device must be 'cpu', 'mps', or start with 'cuda' (e.g., 'cuda' or 'cuda:0')")

        valid_stores = {"faiss", "chroma", "annoy", "none"}
        if self.vector_store not in valid_stores:
            raise ValueError(
                f"vector_store must be one of {sorted(valid_stores)}")

        if self.index_path is not None:
            parent = self.index_path.parent if self.index_path.suffix else self.index_path
            if not parent.exists():
                if self.create_missing:
                    parent.mkdir(parents=True, exist_ok=True)
                else:
                    raise ValueError(f"Path does not exist: {parent}")
            if self.index_path.exists() and self.index_path.is_dir() and self.index_path.suffix:
                raise ValueError(
                    "index_path points to a directory but looks like a file path (has a suffix)")

        if self.data_dir is not None:
            if not self.data_dir.exists():
                if self.create_missing:
                    self.data_dir.mkdir(parents=True, exist_ok=True)
                else:
                    raise ValueError(
                        f"data_dir does not exist: {self.data_dir}")
            if not self.data_dir.is_dir():
                raise ValueError(
                    f"data_dir must be a directory: {self.data_dir}")

        if self.cache_dir is not None:
            if not self.cache_dir.exists():
                if self.create_missing:
                    self.cache_dir.mkdir(parents=True, exist_ok=True)
                else:
                    raise ValueError(
                        f"cache_dir does not exist: {self.cache_dir}")
            if not self.cache_dir.is_dir():
                raise ValueError(
                    f"cache_dir must be a directory: {self.cache_dir}")

        if self.model is not None and not isinstance(self.model, str):
            raise ValueError("model must be a string")

        if self.embedding_model is not None and not isinstance(self.embedding_model, str):
            raise ValueError("embedding_model must be a string")

        if self.seed is not None and (not isinstance(self.seed, int) or self.seed < 0):
            raise ValueError("seed must be a non-negative integer")

        if self.include_patterns is not None and not all(isinstance(p, str) for p in self.include_patterns):
            raise ValueError("include_patterns must be a list of strings")

        if self.exclude_patterns is not None and not all(isinstance(p, str) for p in self.exclude_patterns):
            raise ValueError("exclude_patterns must be a list of strings")

    @staticmethod
    def _get(args: argparse.Namespace, names: Iterable[str], default: Any) -> Any:
        for name in names:
            if hasattr(args, name):
                val = getattr(args, name)
                if val is not None:
                    return val
        return default

    @staticmethod
    def _as_bool(v: Any) -> bool:
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            return v.strip().lower() in {"1", "true", "yes", "y", "on"}
        if isinstance(v, (int, float)):
            return bool(v)
        return False

    @staticmethod
    def _maybe_int(v: Any) -> Optional[int]:
        if v is None:
            return None
        if isinstance(v, int):
            return v
        try:
            return int(v)
        except Exception:
            return None

    @staticmethod
    def _maybe_float(v: Any) -> Optional[float]:
        if v is None:
            return None
        if isinstance(v, float):
            return v
        try:
            return float(v)
        except Exception:
            return None

    @staticmethod
    def _as_list(v: Any) -> Optional[List[str]]:
        if v is None:
            return None
        if isinstance(v, (list, tuple)):
            return [str(x) for x in v]
        if isinstance(v, str):
            parts = [p.strip() for p in v.split(",")]
            return [p for p in parts if p]
        return None

    @staticmethod
    def _path(v: Optional[Union[str, Path]], is_dir: bool = False) -> Optional[Path]:
        if v is None:
            return None
        p = Path(v).expanduser()
        if not is_dir and p.is_dir():
            return p
        return p

    @staticmethod
    def _lower_or_none(v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        return str(v).lower()
