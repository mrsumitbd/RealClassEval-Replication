from dataclasses import dataclass
import re
from functools import total_ordering

@dataclass
@total_ordering
class IdaVersion:
    product: str
    major: int
    minor: int
    suffix: str | None = None

    @classmethod
    def from_installer_filename(cls, filename: str):
        """Parse IDA installer filename to extract version information.

        Args:
            filename: IDA installer filename (e.g., 'ida-pro_92_x64linux.run')

        Raises:
            ValueError: If filename format is not recognized
        """
        basename = filename
        for ext in ['.app.zip', '.run', '.exe']:
            if basename.endswith(ext):
                basename = basename[:-len(ext)]
                break
        match = re.match('^ida-([^_]+)_(\\d{2})(sp\\d+)?_', basename)
        if not match:
            raise ValueError(f'Unrecognized installer filename format: {filename}')
        product_part = match.group(1)
        version_major = int(match.group(2)[0])
        version_minor = int(match.group(2)[1])
        suffix = match.group(3) if match.group(3) else None
        product_mapping = {'pro': 'IDA Professional', 'home-pc': 'IDA Home', 'home-arm': 'IDA Home', 'home-mips': 'IDA Home', 'home-ppc': 'IDA Home', 'home-riscv': 'IDA Home', 'free-pc': 'IDA Free', 'essential': 'IDA Essential', 'classroom-free': 'IDA Classroom'}
        product = product_mapping.get(product_part, f'IDA {product_part.title()}')
        return cls(product, version_major, version_minor, suffix)

    def __str__(self):
        base = f'{self.product} {self.major}.{self.minor}'
        return f'{base}{self.suffix}' if self.suffix else base

    def __lt__(self, other):
        if not isinstance(other, IdaVersion):
            return NotImplemented
        return (self.product, self.major, self.minor, self.suffix or '') < (other.product, other.major, other.minor, other.suffix or '')