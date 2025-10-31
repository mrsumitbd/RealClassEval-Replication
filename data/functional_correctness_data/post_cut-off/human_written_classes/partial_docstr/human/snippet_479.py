import subprocess
import json
from pathlib import Path

class BranchManager:
    """Manages versions across main and mcp-remote branches safely."""

    def __init__(self):
        self.repo_root = Path(__file__).parent.parent
        self.branches_info = {'main': {'version': '2.1.0', 'transport': 'stdio', 'pyproject_path': 'pyproject.toml'}, 'mcp-remote': {'version': '3.0.0', 'transport': 'remote', 'pyproject_path': 'pyproject.toml'}}

    def get_current_branch(self) -> str:
        """Get current git branch."""
        try:
            result = subprocess.run(['git', 'branch', '--show-current'], capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return 'unknown'

    def get_version_from_pyproject(self) -> str:
        """Get version from current pyproject.toml."""
        pyproject_path = self.repo_root / 'pyproject.toml'
        if not pyproject_path.exists():
            return 'unknown'
        try:
            import tomllib
            with open(pyproject_path, 'rb') as f:
                data = tomllib.load(f)
            return data.get('project', {}).get('version', 'unknown')
        except ImportError:
            try:
                import toml
                with open(pyproject_path) as f:
                    data = toml.load(f)
                return data.get('project', {}).get('version', 'unknown')
            except ImportError:
                pass
        except Exception:
            pass
        try:
            with open(pyproject_path) as f:
                for line in f:
                    if line.startswith('version = '):
                        return line.split('"')[1]
        except:
            pass
        return 'unknown'

    def show_status(self):
        """Show current branch and version status."""
        current_branch = self.get_current_branch()
        current_version = self.get_version_from_pyproject()
        print('📊 Branch Status:')
        print('=' * 30)
        print(f'Current Branch: {current_branch}')
        print(f'Current Version: {current_version}')
        print()
        print('📋 Expected Versions:')
        for branch, info in self.branches_info.items():
            status = '✅ CURRENT' if branch == current_branch else ''
            print(f"{branch:12} v{info['version']} ({info['transport']}) {status}")

    def bump_version(self, new_version: str):
        """Bump version in current branch."""
        current_branch = self.get_current_branch()
        pyproject_path = self.repo_root / 'pyproject.toml'
        if not pyproject_path.exists():
            print(f'❌ No pyproject.toml found in {current_branch} branch')
            return
        with open(pyproject_path, 'r') as f:
            content = f.read()
        old_version = self.get_version_from_pyproject()
        content = content.replace(f'version = "{old_version}"', f'version = "{new_version}"')
        with open(pyproject_path, 'w') as f:
            f.write(content)
        if current_branch in self.branches_info:
            self.branches_info[current_branch]['version'] = new_version
        print(f'✅ Updated {current_branch} from v{old_version} to v{new_version}')

    def create_version_tag(self, version: str=None):
        """Create git tag for current version."""
        current_branch = self.get_current_branch()
        if not version:
            version = self.get_version_from_pyproject()
        transport = self.branches_info.get(current_branch, {}).get('transport', 'unknown')
        tag_name = f'{transport}-v{version}'
        try:
            subprocess.run(['git', 'tag', tag_name], check=True)
            print(f'✅ Created tag: {tag_name}')
        except subprocess.CalledProcessError:
            print(f'❌ Failed to create tag: {tag_name}')

    def save_state(self):
        """Save current branch state to file."""
        state_file = self.repo_root / '.version-state.json'
        current_branch = self.get_current_branch()
        current_version = self.get_version_from_pyproject()
        state = {'last_update': str(subprocess.check_output(['date'], text=True).strip()), 'current_branch': current_branch, 'branches': self.branches_info.copy()}
        if current_branch in state['branches']:
            state['branches'][current_branch]['version'] = current_version
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2)
        print(f'💾 Saved state to {state_file}')