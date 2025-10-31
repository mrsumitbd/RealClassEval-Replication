import dataclasses
from textwrap import dedent

@dataclasses.dataclass
class Example:
    section_complete: str = ''
    cfg: str = ''
    pyproject_toml: str = ''
    cli: str = ''

    def __post_init__(self):
        if self.cfg or self.pyproject_toml or self.cli:
            if self.cfg:
                cfg = dedent(self.cfg).lstrip()
                self.cfg = dedent('\n                    ### Example `.isort.cfg`\n\n                    ```\n                    [settings]\n                    {cfg}\n                    ```\n                    ').format(cfg=cfg).lstrip()
            if self.pyproject_toml:
                pyproject_toml = dedent(self.pyproject_toml).lstrip()
                self.pyproject_toml = dedent('\n                    ### Example `pyproject.toml`\n\n                    ```\n                    [tool.isort]\n                    {pyproject_toml}\n                    ```\n                    ').format(pyproject_toml=pyproject_toml).lstrip()
            if self.cli:
                cli = dedent(self.cli).lstrip()
                self.cli = dedent('\n                    ### Example cli usage\n\n                    `{cli}`\n                    ').format(cli=cli).lstrip()
            sections = [s for s in [self.cfg, self.pyproject_toml, self.cli] if s]
            sections_str = '\n'.join(sections)
            self.section_complete = f'**Examples:**\n\n{sections_str}'
        else:
            self.section_complete = ''

    def __str__(self):
        return self.section_complete