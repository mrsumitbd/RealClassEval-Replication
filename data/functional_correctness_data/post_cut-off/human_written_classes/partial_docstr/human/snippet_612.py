from pathlib import Path
import yaml
from typing import Any

class IssueplanValidator:
    """Validates issue plan files for proper structure and content."""
    REQUIRED_FIELDS = {'issue_num': int, 'flow_name': str, 'pattern': str, 'project_phase': str, 'is_critical_path': bool, 'is_experimental': bool, 'blocks_issues': list, 'enables_issues': list, 'dependencies': list, 'workspace_path': str}
    VALID_PATTERNS = ['FANOUT', 'W_REFINEMENT']
    VALID_PHASES = ['exploration', 'development', 'integration', 'production']
    REFINEMENT_FIELDS = {'refinement_enabled': bool, 'refinement_desc': str, 'critic_domain': str, 'gate_instruction': str, 'gates': list}

    def __init__(self):
        self.errors = []
        self.warnings = []

    def validate_file(self, file_path: Path) -> bool:
        """Validate a single issue plan file."""
        self.errors.clear()
        self.warnings.clear()
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            self.errors.append(f'Could not read file: {e}')
            return False
        if not content.startswith('---'):
            self.errors.append('File must start with YAML frontmatter (---)')
            return False
        parts = content.split('---', 2)
        if len(parts) < 3:
            self.errors.append('Invalid YAML frontmatter structure')
            return False
        yaml_content = parts[1].strip()
        markdown_content = parts[2].strip()
        try:
            metadata = yaml.safe_load(yaml_content)
        except yaml.YAMLError as e:
            self.errors.append(f'Invalid YAML: {e}')
            return False
        if not isinstance(metadata, dict):
            self.errors.append('YAML frontmatter must be a dictionary')
            return False
        self._validate_required_fields(metadata)
        self._validate_field_types(metadata)
        self._validate_pattern_requirements(metadata)
        self._validate_markdown_content(markdown_content, metadata)
        return len(self.errors) == 0

    def _validate_required_fields(self, metadata: dict[str, Any]):
        """Check all required fields are present."""
        for field in self.REQUIRED_FIELDS:
            if field not in metadata:
                self.errors.append(f'Missing required field: {field}')

    def _validate_field_types(self, metadata: dict[str, Any]):
        """Validate field types and values."""
        for field, expected_type in self.REQUIRED_FIELDS.items():
            if field not in metadata:
                continue
            value = metadata[field]
            if not isinstance(value, expected_type):
                self.errors.append(f"Field '{field}' must be {expected_type.__name__}, got {type(value).__name__}")
            if field == 'pattern' and value not in self.VALID_PATTERNS:
                self.errors.append(f"Pattern must be one of {self.VALID_PATTERNS}, got '{value}'")
            if field == 'project_phase' and value not in self.VALID_PHASES:
                self.errors.append(f"Project phase must be one of {self.VALID_PHASES}, got '{value}'")
            if field == 'issue_num' and isinstance(value, int) and (value <= 0):
                self.errors.append(f'Issue number must be positive, got {value}')

    def _validate_pattern_requirements(self, metadata: dict[str, Any]):
        """Validate pattern-specific requirements."""
        pattern = metadata.get('pattern')
        if pattern == 'W_REFINEMENT':
            has_refinement_config = any((field in metadata for field in self.REFINEMENT_FIELDS))
            if not has_refinement_config:
                self.warnings.append('W_REFINEMENT pattern should include refinement configuration')
            else:
                for field, expected_type in self.REFINEMENT_FIELDS.items():
                    if field in metadata:
                        value = metadata[field]
                        if not isinstance(value, expected_type):
                            self.errors.append(f"Refinement field '{field}' must be {expected_type.__name__}")

    def _validate_markdown_content(self, content: str, metadata: dict[str, Any]):
        """Validate markdown content structure."""
        issue_num = metadata.get('issue_num', 'N/A')
        required_sections = [f'# Issue #{issue_num}:', '## System Prompt', '## Description', '## Planning Instructions', '## Synthesis Instructions', '## Context']
        for section in required_sections:
            if section not in content:
                self.errors.append(f'Missing required section: {section}')

    def validate_directory(self, directory: Path) -> dict[str, bool]:
        """Validate all .md files in a directory."""
        results = {}
        if not directory.exists():
            print(f'Directory does not exist: {directory}')
            return results
        md_files = list(directory.glob('*.md'))
        if not md_files:
            print(f'No .md files found in {directory}')
            return results
        for file_path in md_files:
            print(f'Validating {file_path.name}...')
            is_valid = self.validate_file(file_path)
            results[str(file_path)] = is_valid
            if is_valid:
                print('  ✅ Valid')
            else:
                print('  ❌ Invalid')
                for error in self.errors:
                    print(f'    Error: {error}')
            if self.warnings:
                for warning in self.warnings:
                    print(f'    Warning: {warning}')
            print()
        return results