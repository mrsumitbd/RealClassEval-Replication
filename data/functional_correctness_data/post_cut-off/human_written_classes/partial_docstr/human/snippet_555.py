import subprocess
import logging
import sys

class LibVersionBumper:

    def __init__(self) -> None:
        self.valid_bump_types = ['major', 'minor', 'patch']
        self._sync_with_remote()

    @staticmethod
    def get_current_version() -> tuple[str, tuple[int, int, int]]:
        """Get the current version from git tags."""
        try:
            result = subprocess.run(['git', 'describe', '--tags', '--abbrev=0'], capture_output=True, text=True, check=True)
            current_version = result.stdout.strip().lstrip('v')
            major, minor, patch = map(int, current_version.split('.'))
            return (current_version, (major, minor, patch))
        except subprocess.CalledProcessError:
            logging.exception('No existing tags found. Starting from v0.0.0')
            return ('0.0.0', (0, 0, 0))
        except ValueError as e:
            logging.exception(f'Error parsing version: {e}')
            sys.exit(1)

    @staticmethod
    def calculate_new_version(current_version: tuple[int, int, int], bump_type: str) -> str:
        """Calculate the new version based on bump type."""
        major, minor, patch = current_version
        if bump_type == 'major':
            new_version = (major + 1, 0, 0)
        elif bump_type == 'minor':
            new_version = (major, minor + 1, 0)
        elif bump_type == 'patch':
            new_version = (major, minor, patch + 1)
        else:
            raise ValueError(f'Invalid bump type: {bump_type}')
        return '.'.join(map(str, new_version))

    def create_and_push_tag(self, new_version: str, message: str | None=None) -> None:
        """Create and push a new git tag."""
        try:
            self._sync_with_remote(tags_only=True)
            tag_version = f'v{new_version}'
            result = subprocess.run(['git', 'tag', '-l', tag_version], capture_output=True, text=True, check=True)
            if tag_version in result.stdout:
                logging.info(f'Tag {tag_version} already exists!')
                sys.exit(1)
            tag_message = message or f'Release {tag_version}'
            subprocess.run(['git', 'tag', '-a', tag_version, '-m', tag_message], check=True)
            subprocess.run(['git', 'push', 'origin', tag_version], check=True)
            logging.info(f'Successfully created and pushed tag: {tag_version}')
            logging.info(f'Tag message: {tag_message}')
        except subprocess.CalledProcessError as e:
            logging.exception(f'Error in git operations: {e}')
            sys.exit(1)

    def bump_version(self, bump_type: str, message: str | None=None) -> None:
        """Main function to bump version."""
        if bump_type not in self.valid_bump_types:
            logging.info(f'Invalid bump type. Must be one of: {self.valid_bump_types}')
            sys.exit(1)
        current_version_str, current_version_tuple = self.get_current_version()
        logging.info(f'Current version: {current_version_str}')
        new_version = self.calculate_new_version(current_version_tuple, bump_type)
        logging.info(f'New version will be: {new_version}')
        logging.info(f'Tag message will be: {message}')
        if input('Proceed with version bump? [y/N]: ').lower() != 'y':
            logging.info('Version bump cancelled.')
            sys.exit(0)
        self.create_and_push_tag(new_version, message)

    @staticmethod
    def _sync_with_remote(tags_only: bool=False) -> None:
        """Sync with remote repository."""
        if tags_only:
            subprocess.run(['git', 'fetch', '--tags'], capture_output=True, text=True, check=True)
        else:
            subprocess.run(['git', 'fetch', '--all'], capture_output=True, text=True, check=True)