from pathlib import Path
from typing import Dict, Optional

class PromptCompiler:
    """Compiles .prompt.md files with parameter substitution."""

    def __init__(self):
        """Initialize compiler."""
        self.compiled_dir = Path('.apm/compiled')

    def compile(self, prompt_file: str, params: Dict[str, str]) -> str:
        """Compile a .prompt.md file with parameter substitution.

        Args:
            prompt_file: Path to the .prompt.md file
            params: Parameters to substitute

        Returns:
            Path to the compiled file
        """
        prompt_path = Path(prompt_file)
        if not prompt_path.exists():
            raise FileNotFoundError(f'Prompt file not found: {prompt_file}')
        self.compiled_dir.mkdir(parents=True, exist_ok=True)
        with open(prompt_path, 'r') as f:
            content = f.read()
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = parts[1].strip()
                main_content = parts[2].strip()
            else:
                main_content = content
        else:
            main_content = content
        compiled_content = self._substitute_parameters(main_content, params)
        output_name = prompt_path.stem.replace('.prompt', '') + '.txt'
        output_path = self.compiled_dir / output_name
        with open(output_path, 'w') as f:
            f.write(compiled_content)
        return str(output_path)

    def _substitute_parameters(self, content: str, params: Dict[str, str]) -> str:
        """Substitute parameters in content.

        Args:
            content: Content to process
            params: Parameters to substitute

        Returns:
            Content with parameters substituted
        """
        result = content
        for key, value in params.items():
            placeholder = f'${{input:{key}}}'
            result = result.replace(placeholder, str(value))
        return result