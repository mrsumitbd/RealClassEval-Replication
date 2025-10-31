import argparse

class BaseBenchmark:
    """Base parser class for benchmarking kernels."""

    def __init__(self, description: str='Benchmarking CLI for Wave kernels', epilog: str='', formatter_class=argparse.RawTextHelpFormatter):
        self.parser = argparse.ArgumentParser(description=description, epilog=epilog, formatter_class=formatter_class)
        self._add_common_args()

    def _add_common_args(self) -> None:
        self.parser.add_argument('--output', type=str, default=DEFAULT_OUTPUT_FILENAME, help='Path to output trace file')
        self.parser.add_argument('--config', type=str, required=True, help='Path to JSON config file')
        self.parser.add_argument('--num_warmup', type=int, default=10, help='Number of warmup iterations')
        self.parser.add_argument('--num_iterations', type=int, default=100, help='Number of benchmark iterations')

    def parse(self):
        return self.parser.parse_args()