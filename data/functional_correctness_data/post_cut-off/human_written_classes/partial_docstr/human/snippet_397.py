import re
from pathlib import Path

class SystemVerilogValidator:
    """Validates SystemVerilog template files for common syntax issues."""

    def __init__(self):
        self.errors = []
        self.warnings = []
        self.templates_dir = Path('src/templates/sv')
        self.systemverilog_constructs = {'always_ff': 'Use "always @(posedge clk)" instead for better compatibility', 'always_comb': 'Use "always @(*)" instead for better compatibility', 'logic': 'Consider using "wire" or "reg" for better compatibility', 'bit': 'OK for PCILeech compatibility (used in reference code)', 'interface': 'SystemVerilog interface - ensure project is configured for SystemVerilog'}
        self.problematic_patterns = [('\\binput\\s+\\w+\\s+\\w+.*?;', 'Standalone input declaration found outside module ports'), ('\\boutput\\s+\\w+\\s+\\w+.*?;', 'Standalone output declaration found outside module ports'), ('\\binout\\s+\\w+\\s+\\w+.*?;', 'Standalone inout declaration found outside module ports')]

    def validate_file(self, filepath: Path) -> bool:
        """Validate a single SystemVerilog template file."""
        print(f'Validating: {filepath}')
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            self.errors.append(f'{filepath}: Failed to read file - {e}')
            return False
        file_valid = True
        if not self._check_module_structure(filepath, content):
            file_valid = False
        if not self._check_standalone_ports(filepath, content):
            file_valid = False
        self._check_systemverilog_constructs(filepath, content)
        if not self._check_template_syntax(filepath, content):
            file_valid = False
        return file_valid

    def _check_module_structure(self, filepath: Path, content: str) -> bool:
        """Check if file has proper module structure."""
        include_patterns = ['register_declarations', 'error_outputs', 'device_specific_ports', 'clock_domain_logic', 'interrupt_logic', 'read_logic', 'write_logic', 'error_declarations', 'error_detection', 'error_handling', 'error_logging', 'error_state_machine', 'error_injection', 'error_counters', 'error_handling_complete', 'power_integration', 'power_management', 'power_declarations', 'performance_counters', 'register_logic']
        if any((pattern in filepath.stem for pattern in include_patterns)):
            return True
        module_match = re.search('\\bmodule\\s+(\\w+)', content)
        endmodule_match = re.search('\\bendmodule\\b', content)
        if not module_match:
            self.errors.append(f'{filepath}: No module declaration found')
            return False
        if not endmodule_match:
            self.errors.append(f'{filepath}: No endmodule found')
            return False
        if module_match.start() > endmodule_match.start():
            self.errors.append(f'{filepath}: endmodule appears before module declaration')
            return False
        return True

    def _check_standalone_ports(self, filepath: Path, content: str) -> bool:
        """Check for problematic standalone port declarations."""
        valid = True
        module_match = re.search('\\bmodule\\s+\\w+.*?\\(.*?\\);', content, re.DOTALL)
        if not module_match:
            return True
        module_end = module_match.end()
        endmodule_match = re.search('\\bendmodule\\b', content)
        if endmodule_match:
            module_body = content[module_end:endmodule_match.start()]
        else:
            module_body = content[module_end:]
        clean_body = module_body
        clean_body = re.sub('\\bfunction\\s+.*?\\bendfunction\\b', '', clean_body, flags=re.DOTALL)
        clean_body = re.sub('\\btask\\s+.*?\\bendtask\\b', '', clean_body, flags=re.DOTALL)
        for pattern, message in self.problematic_patterns:
            matches = re.finditer(pattern, clean_body, re.MULTILINE)
            for match in matches:
                line_num = content[:module_end + match.start()].count('\n') + 1
                self.errors.append(f'{filepath}:{line_num}: {message}')
                valid = False
        return valid

    def _check_systemverilog_constructs(self, filepath: Path, content: str):
        """Check for SystemVerilog-specific constructs and provide guidance."""
        for construct, guidance in self.systemverilog_constructs.items():
            if construct in content:
                if construct == 'logic' and 'bit' not in content:
                    self.warnings.append(f"{filepath}: Uses '{construct}' - {guidance}")
                elif construct == 'interface':
                    self.warnings.append(f"{filepath}: Uses '{construct}' - {guidance}")

    def _check_template_syntax(self, filepath: Path, content: str) -> bool:
        """Check basic Jinja2 template syntax."""
        open_braces = content.count('{{')
        close_braces = content.count('}}')
        if open_braces != close_braces:
            self.errors.append(f'{filepath}: Unmatched template braces ({{ vs }})')
            return False
        open_blocks = len(re.findall('{%\\s*(?:if|for|macro)', content))
        close_blocks = len(re.findall('{%\\s*end(?:if|for|macro)', content))
        if open_blocks != close_blocks:
            self.errors.append(f'{filepath}: Unmatched template control blocks')
            return False
        return True

    def validate_all_templates(self) -> bool:
        """Validate all SystemVerilog templates."""
        if not self.templates_dir.exists():
            self.errors.append(f'Templates directory not found: {self.templates_dir}')
            return False
        template_files = list(self.templates_dir.glob('*.sv.j2'))
        if not template_files:
            self.warnings.append('No SystemVerilog template files found')
            return True
        print(f'Found {len(template_files)} SystemVerilog template files')
        all_valid = True
        for template_file in template_files:
            if not self.validate_file(template_file):
                all_valid = False
        return all_valid

    def print_results(self):
        """Print validation results."""
        if self.errors:
            print(f'\n❌ Found {len(self.errors)} errors:')
            for error in self.errors:
                print(f'   {error}')
        if self.warnings:
            print(f'\n⚠️  Found {len(self.warnings)} warnings:')
            for warning in self.warnings:
                print(f'   {warning}')
        if not self.errors and (not self.warnings):
            print('\n✅ All SystemVerilog templates passed validation!')
        elif not self.errors:
            print(f'\n✅ All SystemVerilog templates are valid (with {len(self.warnings)} warnings)')
        else:
            print(f'\n❌ Validation failed with {len(self.errors)} errors and {len(self.warnings)} warnings')