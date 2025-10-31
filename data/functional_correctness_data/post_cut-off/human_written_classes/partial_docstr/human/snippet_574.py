from blockscout_mcp_server.config import config
from blockscout_mcp_server.models import ChainInfo
import time
import anyio

class ChainsListCache:
    """In-process TTL cache for the chains list."""

    def __init__(self) -> None:
        self.chains_snapshot: list[ChainInfo] | None = None
        self.expiry_timestamp: float = 0.0
        self.lock = anyio.Lock()

    def get_if_fresh(self) -> list[ChainInfo] | None:
        """Return cached chains if the snapshot is still fresh."""
        if self.chains_snapshot is None or time.monotonic() >= self.expiry_timestamp:
            return None
        return self.chains_snapshot

    def needs_refresh(self) -> bool:
        """Return ``True`` if the snapshot is missing or expired."""
        return self.get_if_fresh() is None

    def store_snapshot(self, chains: list[ChainInfo]) -> None:
        """Store a fresh snapshot and compute its expiry timestamp."""
        self.chains_snapshot = chains
        self.expiry_timestamp = time.monotonic() + config.chains_list_ttl_seconds