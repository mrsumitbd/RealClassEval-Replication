from pathlib import Path
import subprocess
from typing import Dict, List

class VersionManager:
    """Manages versions across multiple packages."""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.packages_dir = repo_root / 'packages'

    def get_package_version(self, package: str) -> str:
        """Get current version of a package."""
        pyproject_path = self.packages_dir / package / 'pyproject.toml'
        if not pyproject_path.exists():
            return '0.0.0'
        try:
            if hasattr(tomllib, 'load'):
                with open(pyproject_path, 'rb') as f:
                    data = tomllib.load(f)
            else:
                with open(pyproject_path) as f:
                    for line in f:
                        if line.strip().startswith('version = '):
                            return line.split('"')[1]
                return '0.0.0'
        except Exception:
            return '0.0.0'
        return data.get('project', {}).get('version', '0.0.0')

    def set_package_version(self, package: str, version: str):
        """Set version for a package."""
        pyproject_path = self.packages_dir / package / 'pyproject.toml'
        with open(pyproject_path, 'r') as f:
            content = f.read()
        import re
        pattern = 'version = "[^"]*"'
        replacement = f'version = "{version}"'
        content = re.sub(pattern, replacement, content)
        with open(pyproject_path, 'w') as f:
            f.write(content)
        print(f'✓ Updated {package} to v{version}')

    def get_all_versions(self) -> Dict[str, str]:
        """Get versions of all packages."""
        packages = ['core', 'stdio', 'remote']
        return {pkg: self.get_package_version(pkg) for pkg in packages}

    def update_core_dependencies(self, core_version: str):
        """Update core dependency version in transport packages."""
        transport_packages = ['stdio', 'remote']
        for package in transport_packages:
            pyproject_path = self.packages_dir / package / 'pyproject.toml'
            if not pyproject_path.exists():
                continue
            with open(pyproject_path, 'r') as f:
                content = f.read()
            major_version = core_version.split('.')[0]
            next_major = str(int(major_version) + 1)
            new_dep = f'wazuh-mcp-core>={core_version},<{next_major}.0.0'
            import re
            pattern = 'wazuh-mcp-core[>=<,\\.\\d]*'
            content = re.sub(pattern, new_dep, content)
            with open(pyproject_path, 'w') as f:
                f.write(content)
            print(f'✓ Updated {package} core dependency to >={core_version}')

    def tag_release(self, package: str, version: str):
        """Create git tag for package release."""
        tag_name = f'{package}-v{version}'
        try:
            subprocess.run(['git', 'tag', tag_name], check=True)
            print(f'✓ Created tag {tag_name}')
        except subprocess.CalledProcessError:
            print(f'❌ Failed to create tag {tag_name}')