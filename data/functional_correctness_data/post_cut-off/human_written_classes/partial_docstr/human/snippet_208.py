from pathlib import Path
from typing import Any, Dict, List, Optional
import yaml

class AnvilConfig:
    """Configuration loader for Anvil EVM environment."""

    def __init__(self, config_file: str='configs/token_transfers.yaml'):
        self.config_file = Path(__file__).parent / config_file
        self._raw_config = self._load_config()
        self.anvil = ConfigDict(self._raw_config.get('network', {}))
        self.timeouts = ConfigDict(self._raw_config.get('timeouts', {}))
        self.funding = ConfigDict(self._raw_config.get('funding', {}))
        self.whitelisted_tokens = ConfigDict(self._raw_config.get('whitelisted_tokens', {}))
        self.defi = ConfigDict(self._raw_config.get('defi', {}))
        self.swaps = ConfigDict(self._raw_config.get('swaps', {}))

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(self.config_file, 'r') as f:
                config = yaml.safe_load(f)
            return config
        except FileNotFoundError:
            raise FileNotFoundError(f'Configuration file not found: {self.config_file}')
        except yaml.YAMLError as e:
            raise ValueError(f'Error parsing configuration file: {e}')

    def get_rpc_url(self) -> str:
        """Get the full RPC URL for the Anvil instance."""
        return f'http://127.0.0.1:{self.anvil.port}'

    def get_anvil_startup_command(self, port: int=None, fork_url: str=None) -> list[str]:
        """Get the Anvil startup command with specified or default parameters."""
        cmd = ['anvil', '--port', str(port or self.anvil.port)]
        if fork_url or self.anvil.fork_url:
            cmd += ['--fork-url', fork_url or self.anvil.fork_url]
        return cmd