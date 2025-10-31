from pathlib import Path
import re
from dataclasses import dataclass, field

@dataclass
class CommitConfig:
    project_root: Path
    default_push: bool = True
    allow_empty_commits: bool = False
    conventional_commit_types: list[str] = field(default_factory=lambda: ['feat', 'fix', 'build', 'chore', 'ci', 'docs', 'perf', 'refactor', 'revert', 'style', 'test'])
    conventional_commit_regex_pattern: str | None = None
    fallback_git_user_name: str = 'khive-bot'
    fallback_git_user_email: str = 'khive-bot@example.com'
    default_stage_mode: str = 'all'
    json_output: bool = False
    dry_run: bool = False
    verbose: bool = False

    @property
    def khive_config_dir(self) -> Path:
        return self.project_root / '.khive'

    @property
    def conventional_commit_regex(self) -> re.Pattern:
        if self.conventional_commit_regex_pattern:
            return re.compile(self.conventional_commit_regex_pattern)
        types_str = '|'.join(map(re.escape, self.conventional_commit_types))
        return re.compile(f'^(?:{types_str})(?:\\([\\w-]+\\))?(?:!)?: .+')