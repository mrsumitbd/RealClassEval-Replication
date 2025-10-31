from pathlib import Path
from rich import print
from cookiecutter.exceptions import RepositoryNotFound
import typer
from cookiecutter.main import cookiecutter

class ProjectInitializer:
    """Handles the logic for the 'init' command."""

    def __init__(self, project_name, template, checkout):
        self.project_name = project_name
        self.template = template
        self.checkout = checkout
        self.project_path = None

    def run(self):
        """Executes the entire project initialization workflow."""
        try:
            self._create_from_template()
            self._print_final_summary()
        except RepositoryNotFound:
            print(f'[bold red]\n❌ Error: Repository not found at {REPO_URL}[/bold red]')
            print('[bold red]\nPlease check the URL and your network connection.[/bold red]')
            raise typer.Exit()
        except Exception as e:
            print(f'[bold red]\nAn unexpected error occurred: {e}[/bold red]')
            raise typer.Exit()

    def _create_from_template(self):
        """Builds the project using Cookiecutter."""
        print(f'[bold green]🚀 Initializing project from Git repository: {REPO_URL}[/bold green]')
        template_dir = f'templates/{self.template}'
        created_path = cookiecutter(REPO_URL, directory=template_dir, checkout=self.checkout, extra_context={'project_slug': self.project_name}, output_dir='.')
        self.project_path = Path(created_path)
        print(f'[bold green]✅ Project created at {self.project_path}[/bold green]')

    def _print_final_summary(self):
        """Prints the final success message and next steps."""
        final_project_name = self.project_path.name
        print('[bold green]\n🎉 Project initialized successfully![/bold green]')
        print('\nNext steps:')
        print(f'  1. Change into the project directory: cd {final_project_name}')
        print('  2. Start all services: dingent run')