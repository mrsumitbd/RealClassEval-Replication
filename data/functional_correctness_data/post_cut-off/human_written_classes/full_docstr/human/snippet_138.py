from pathlib import Path
from golf.core.parser import ComponentType, ParsedComponent, parse_project
import json
from typing import Any
from golf.core.config import Settings

class ManifestBuilder:
    """Builds FastMCP manifest from parsed components."""

    def __init__(self, project_path: Path, settings: Settings) -> None:
        """Initialize the manifest builder.

        Args:
            project_path: Path to the project root
            settings: Project settings
        """
        self.project_path = project_path
        self.settings = settings
        self.components: dict[ComponentType, list[ParsedComponent]] = {}
        self.manifest: dict[str, Any] = {'name': settings.name, 'description': settings.description or '', 'tools': [], 'resources': [], 'prompts': []}

    def build(self) -> dict[str, Any]:
        """Build the complete manifest.

        Returns:
            FastMCP manifest dictionary
        """
        self.components = parse_project(self.project_path)
        self._process_tools()
        self._process_resources()
        self._process_prompts()
        return self.manifest

    def _process_tools(self) -> None:
        """Process all tool components and add them to the manifest."""
        for component in self.components[ComponentType.TOOL]:
            input_properties = {}
            required_fields = []
            if component.input_schema and 'properties' in component.input_schema:
                input_properties = component.input_schema['properties']
                if 'required' in component.input_schema:
                    required_fields = component.input_schema['required']
            tool_schema = {'name': component.name, 'description': component.docstring or '', 'inputSchema': {'type': 'object', 'properties': input_properties, 'additionalProperties': False, '$schema': 'http://json-schema.org/draft-07/schema#'}, 'annotations': {'title': component.name.replace('-', ' ').title()}, 'entry_function': component.entry_function}
            if required_fields:
                tool_schema['inputSchema']['required'] = required_fields
            if component.annotations:
                tool_schema['annotations'].update(component.annotations)
            self.manifest['tools'].append(tool_schema)

    def _process_resources(self) -> None:
        """Process all resource components and add them to the manifest."""
        for component in self.components[ComponentType.RESOURCE]:
            if not component.uri_template:
                console.print(f'[yellow]Warning: Resource {component.name} has no URI template[/yellow]')
                continue
            resource_schema = {'uri': component.uri_template, 'name': component.name, 'description': component.docstring or '', 'entry_function': component.entry_function}
            self.manifest['resources'].append(resource_schema)

    def _process_prompts(self) -> None:
        """Process all prompt components and add them to the manifest."""
        for component in self.components[ComponentType.PROMPT]:
            prompt_schema = {'name': component.name, 'description': component.docstring or '', 'entry_function': component.entry_function}
            if component.parameters:
                arguments = []
                for param in component.parameters:
                    arguments.append({'name': param, 'required': True})
                prompt_schema['arguments'] = arguments
            self.manifest['prompts'].append(prompt_schema)

    def save_manifest(self, output_path: Path | None=None) -> Path:
        """Save the manifest to a JSON file.

        Args:
            output_path: Path to save the manifest to (defaults to .golf/manifest.json)

        Returns:
            Path where the manifest was saved
        """
        if not output_path:
            golf_dir = self.project_path / '.golf'
            golf_dir.mkdir(exist_ok=True)
            output_path = golf_dir / 'manifest.json'
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(self.manifest, f, indent=2)
        console.print(f'[green]Manifest saved to {output_path}[/green]')
        return output_path