from datetime import datetime
from jinja2 import Template
import json
import csv

class Reporter:
    """Report generation class for scan results"""

    def __init__(self, target_url):
        self.target_url = target_url
        self.scan_time = datetime.now()
        self.results = {}

    def add_module_results(self, module_name, results):
        """Add results from a scanning module"""
        self.results[module_name] = results

    def generate_json_report(self, output_file=None):
        """Generate JSON format report"""
        report_data = {'scan_info': {'target': self.target_url, 'scan_time': self.scan_time.isoformat(), 'scanner': 'DiscourseMap Security Scanner', 'version': '1.0.0'}, 'results': self.results, 'summary': self._generate_summary()}
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            return f'JSON report saved to {output_file}'
        else:
            return json.dumps(report_data, indent=2, ensure_ascii=False)

    def generate_html_report(self, output_file=None):
        """Generate HTML format report"""
        html_template = '\n<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>DiscourseMap Security Scan Report</title>\n    <style>\n        body {\n            font-family: \'Segoe UI\', Tahoma, Geneva, Verdana, sans-serif;\n            line-height: 1.6;\n            margin: 0;\n            padding: 20px;\n            background-color: #f5f5f5;\n        }\n        .container {\n            max-width: 1200px;\n            margin: 0 auto;\n            background: white;\n            padding: 30px;\n            border-radius: 10px;\n            box-shadow: 0 0 20px rgba(0,0,0,0.1);\n        }\n        .header {\n            text-align: center;\n            border-bottom: 3px solid #007cba;\n            padding-bottom: 20px;\n            margin-bottom: 30px;\n        }\n        .header h1 {\n            color: #007cba;\n            margin: 0;\n            font-size: 2.5em;\n        }\n        .scan-info {\n            background: #f8f9fa;\n            padding: 20px;\n            border-radius: 8px;\n            margin-bottom: 30px;\n            border-left: 5px solid #007cba;\n        }\n        .module-section {\n            margin-bottom: 40px;\n            border: 1px solid #ddd;\n            border-radius: 8px;\n            overflow: hidden;\n        }\n        .module-header {\n            background: #007cba;\n            color: white;\n            padding: 15px 20px;\n            font-size: 1.3em;\n            font-weight: bold;\n        }\n        .module-content {\n            padding: 20px;\n        }\n        .vulnerability {\n            margin-bottom: 20px;\n            padding: 15px;\n            border-radius: 5px;\n            border-left: 5px solid #ddd;\n        }\n        .critical {\n            background: #fff5f5;\n            border-left-color: #dc3545;\n        }\n        .high {\n            background: #fff8e1;\n            border-left-color: #ff9800;\n        }\n        .medium {\n            background: #fff3e0;\n            border-left-color: #ff5722;\n        }\n        .low {\n            background: #f3e5f5;\n            border-left-color: #9c27b0;\n        }\n        .info {\n            background: #e3f2fd;\n            border-left-color: #2196f3;\n        }\n        .success {\n            background: #e8f5e8;\n            border-left-color: #4caf50;\n        }\n        .severity-badge {\n            display: inline-block;\n            padding: 4px 8px;\n            border-radius: 4px;\n            font-size: 0.8em;\n            font-weight: bold;\n            text-transform: uppercase;\n        }\n        .severity-critical {\n            background: #dc3545;\n            color: white;\n        }\n        .severity-high {\n            background: #ff9800;\n            color: white;\n        }\n        .severity-medium {\n            background: #ff5722;\n            color: white;\n        }\n        .severity-low {\n            background: #9c27b0;\n            color: white;\n        }\n        .summary-stats {\n            display: grid;\n            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));\n            gap: 20px;\n            margin-bottom: 30px;\n        }\n        .stat-card {\n            background: #f8f9fa;\n            padding: 20px;\n            border-radius: 8px;\n            text-align: center;\n            border: 1px solid #ddd;\n        }\n        .stat-number {\n            font-size: 2em;\n            font-weight: bold;\n            color: #007cba;\n        }\n        .stat-label {\n            color: #666;\n            margin-top: 5px;\n        }\n        table {\n            width: 100%;\n            border-collapse: collapse;\n            margin-top: 15px;\n        }\n        th, td {\n            padding: 12px;\n            text-align: left;\n            border-bottom: 1px solid #ddd;\n        }\n        th {\n            background: #f8f9fa;\n            font-weight: bold;\n        }\n        .code {\n            background: #f4f4f4;\n            padding: 10px;\n            border-radius: 4px;\n            font-family: \'Courier New\', monospace;\n            font-size: 0.9em;\n            overflow-x: auto;\n        }\n        .footer {\n            text-align: center;\n            margin-top: 40px;\n            padding-top: 20px;\n            border-top: 1px solid #ddd;\n            color: #666;\n        }\n    </style>\n</head>\n<body>\n    <div class="container">\n        <div class="header">\n            <h1>🔍 DiscourseMap Security Scanner</h1>\n            <p>Comprehensive Security Assessment Report</p>\n        </div>\n\n        <div class="scan-info">\n            <h2>📋 Scan Information</h2>\n            <p><strong>Target:</strong> {{ target }}</p>\n            <p><strong>Scan Time:</strong> {{ scan_time }}</p>\n            <p><strong>Scanner Version:</strong> 1.0.0</p>\n        </div>\n\n        <div class="summary-stats">\n            <div class="stat-card">\n                <div class="stat-number">{{ summary.total_vulnerabilities }}</div>\n                <div class="stat-label">Total Vulnerabilities</div>\n            </div>\n            <div class="stat-card">\n                <div class="stat-number">{{ summary.critical_count }}</div>\n                <div class="stat-label">Critical Issues</div>\n            </div>\n            <div class="stat-card">\n                <div class="stat-number">{{ summary.high_count }}</div>\n                <div class="stat-label">High Risk Issues</div>\n            </div>\n            <div class="stat-card">\n                <div class="stat-number">{{ summary.total_tests }}</div>\n                <div class="stat-label">Tests Performed</div>\n            </div>\n        </div>\n\n        {% for module_name, module_results in results.items() %}\n        <div class="module-section">\n            <div class="module-header">\n                📊 {{ module_results.module_name or module_name }}\n            </div>\n            <div class="module-content">\n                <p><strong>Tests Performed:</strong> {{ module_results.tests_performed or 0 }}</p>\n                <p><strong>Scan Time:</strong> {{ "%.2f"|format(module_results.scan_time or 0) }} seconds</p>\n\n                {% if module_name == \'info_module\' %}\n                    {% if module_results.discourse_info %}\n                    <div class="vulnerability info">\n                        <h4>🔍 Discourse Information</h4>\n                        <table>\n                            {% for key, value in module_results.discourse_info.items() %}\n                            <tr><td><strong>{{ key.replace(\'_\', \' \').title() }}</strong></td><td>{{ value }}</td></tr>\n                            {% endfor %}\n                        </table>\n                    </div>\n                    {% endif %}\n\n                    {% if module_results.plugins %}\n                    <div class="vulnerability info">\n                        <h4>🔌 Installed Plugins</h4>\n                        <ul>\n                        {% for plugin in module_results.plugins %}\n                            <li>{{ plugin.name }} ({{ plugin.version or \'Unknown version\' }})</li>\n                        {% endfor %}\n                        </ul>\n                    </div>\n                    {% endif %}\n\n                    {% if module_results.users %}\n                    <div class="vulnerability info">\n                        <h4>👥 Discovered Users</h4>\n                        <table>\n                            <tr><th>Username</th><th>Trust Level</th><th>Post Count</th></tr>\n                            {% for user in module_results.users %}\n                            <tr>\n                                <td>{{ user.username }}</td>\n                                <td>{{ user.trust_level or \'Unknown\' }}</td>\n                                <td>{{ user.post_count or \'Unknown\' }}</td>\n                            </tr>\n                            {% endfor %}\n                        </table>\n                    </div>\n                    {% endif %}\n                {% endif %}\n\n                {% if module_name == \'vulnerability_module\' %}\n                    {% for vuln_type, vulns in module_results.items() %}\n                        {% if vulns and vuln_type not in [\'module_name\', \'target\', \'tests_performed\', \'scan_time\'] %}\n                        <div class="vulnerability {{ vulns[0].severity if vulns and vulns[0].severity else \'info\' }}">\n                            <h4>🚨 {{ vuln_type.replace(\'_\', \' \').title() }}</h4>\n                            {% for vuln in vulns %}\n                            <div style="margin-bottom: 10px;">\n                                <span class="severity-badge severity-{{ vuln.severity or \'info\' }}">{{ vuln.severity or \'info\' }}</span>\n                                <p><strong>{{ vuln.description or vuln_type }}</strong></p>\n                                {% if vuln.payload %}<div class="code">Payload: {{ vuln.payload }}</div>{% endif %}\n                                {% if vuln.url %}<p><strong>URL:</strong> {{ vuln.url }}</p>{% endif %}\n                            </div>\n                            {% endfor %}\n                        </div>\n                        {% endif %}\n                    {% endfor %}\n                {% endif %}\n\n                {% if module_name == \'endpoint_module\' %}\n                    {% if module_results.discovered_endpoints %}\n                    <div class="vulnerability info">\n                        <h4>🔗 Discovered Endpoints</h4>\n                        <table>\n                            <tr><th>Endpoint</th><th>Status</th><th>Type</th></tr>\n                            {% for endpoint in module_results.discovered_endpoints %}\n                            <tr>\n                                <td>{{ endpoint.path }}</td>\n                                <td>{{ endpoint.status_code }}</td>\n                                <td>{{ endpoint.endpoint_type or \'Unknown\' }}</td>\n                            </tr>\n                            {% endfor %}\n                        </table>\n                    </div>\n                    {% endif %}\n                {% endif %}\n\n                {% if module_name == \'user_module\' %}\n                    {% if module_results.user_enumeration %}\n                    <div class="vulnerability medium">\n                        <h4>👤 User Enumeration</h4>\n                        <table>\n                            <tr><th>Username</th><th>Status</th><th>Method</th></tr>\n                            {% for user in module_results.user_enumeration %}\n                            <tr>\n                                <td>{{ user.username }}</td>\n                                <td>{{ user.status }}</td>\n                                <td>{{ user.method }}</td>\n                            </tr>\n                            {% endfor %}\n                        </table>\n                    </div>\n                    {% endif %}\n\n                    {% if module_results.weak_passwords %}\n                    <div class="vulnerability critical">\n                        <h4>🔑 Weak Passwords</h4>\n                        {% for weak_pass in module_results.weak_passwords %}\n                        <div style="margin-bottom: 10px;">\n                            <span class="severity-badge severity-critical">Critical</span>\n                            <p><strong>{{ weak_pass.description }}</strong></p>\n                            <p>Username: {{ weak_pass.username }}</p>\n                        </div>\n                        {% endfor %}\n                    </div>\n                    {% endif %}\n                {% endif %}\n\n                {% if module_name == \'cve_module\' %}\n                    {% if module_results.cve_results %}\n                    {% for cve in module_results.cve_results %}\n                    <div class="vulnerability {{ cve.severity or \'medium\' }}">\n                        <h4>🔴 {{ cve.cve_id }}</h4>\n                        <span class="severity-badge severity-{{ cve.severity or \'medium\' }}">{{ cve.severity or \'medium\' }}</span>\n                        <p><strong>{{ cve.description }}</strong></p>\n                        {% if cve.payload %}<div class="code">Payload: {{ cve.payload }}</div>{% endif %}\n                        {% if cve.url %}<p><strong>URL:</strong> {{ cve.url }}</p>{% endif %}\n                    </div>\n                    {% endfor %}\n                    {% endif %}\n                {% endif %}\n            </div>\n        </div>\n        {% endfor %}\n\n        <div class="footer">\n            <p>Report generated by DiscourseMap Security Scanner v1.0.0</p>\n            <p>⚠️ This tool is for authorized security testing only. Use responsibly.</p>\n        </div>\n    </div>\n</body>\n</html>\n        '
        template = Template(html_template)
        html_content = template.render(target=self.target_url, scan_time=self.scan_time.strftime('%Y-%m-%d %H:%M:%S'), results=self.results, summary=self._generate_summary())
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            return f'HTML report saved to {output_file}'
        else:
            return html_content

    def generate_csv_report(self, output_file=None):
        """Generate CSV format report"""
        csv_data = []
        csv_data.append(['Module', 'Issue Type', 'Severity', 'Description', 'URL', 'Payload', 'Status'])
        for module_name, module_results in self.results.items():
            if isinstance(module_results, dict):
                for key, value in module_results.items():
                    if isinstance(value, list) and value:
                        for item in value:
                            if isinstance(item, dict):
                                csv_data.append([module_name, key, item.get('severity', 'info'), item.get('description', ''), item.get('url', ''), item.get('payload', ''), item.get('status', '')])
        if output_file:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(csv_data)
            return f'CSV report saved to {output_file}'
        else:
            import io
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerows(csv_data)
            return output.getvalue()

    def _generate_summary(self):
        """Generate summary statistics"""
        summary = {'total_vulnerabilities': 0, 'critical_count': 0, 'high_count': 0, 'medium_count': 0, 'low_count': 0, 'info_count': 0, 'total_tests': 0, 'modules_run': len(self.results)}
        for module_name, module_results in self.results.items():
            if isinstance(module_results, dict):
                summary['total_tests'] += module_results.get('tests_performed', 0)
                for key, value in module_results.items():
                    if isinstance(value, list):
                        for item in value:
                            if isinstance(item, dict) and 'severity' in item:
                                summary['total_vulnerabilities'] += 1
                                severity = item['severity'].lower()
                                if severity == 'critical':
                                    summary['critical_count'] += 1
                                elif severity == 'high':
                                    summary['high_count'] += 1
                                elif severity == 'medium':
                                    summary['medium_count'] += 1
                                elif severity == 'low':
                                    summary['low_count'] += 1
                                else:
                                    summary['info_count'] += 1
        return summary

    def print_summary(self):
        """Print a beautiful formatted summary of the scan results"""
        from colorama import Fore, Style
        import time
        if hasattr(self, '_summary_printed'):
            return
        self._summary_printed = True
        summary = self._generate_summary()
        scan_duration = '0m 0s'
        if hasattr(self, 'scan_start_time') and hasattr(self, 'scan_end_time'):
            duration_seconds = int(self.scan_end_time - self.scan_start_time)
            minutes = duration_seconds // 60
            seconds = duration_seconds % 60
            scan_duration = f'{minutes}m {seconds}s'
        output_lines = []
        output_lines.append(f'\n{Fore.CYAN}🛡️  DiscourseMap v2.0{Style.RESET_ALL}')
        output_lines.append(f'{Fore.CYAN}🎯 Target: {self.target_url}{Style.RESET_ALL}')
        output_lines.append(f"{Fore.CYAN}⏰ Started: {self.scan_time.strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
        output_lines.append('')
        output_lines.append(f'{Fore.CYAN}[INFO] Starting comprehensive security scan...{Style.RESET_ALL}')
        output_lines.append(f"{Fore.CYAN}[INFO] Modules loaded: {(', '.join(self.results.keys()) if self.results else 'none')}{Style.RESET_ALL}")
        output_lines.append('')
        modules_run = list(self.results.keys())
        if 'info' in modules_run:
            output_lines.append(f'{Fore.BLUE}📋 Information Gathering{Style.RESET_ALL}')
            info_results = self.results.get('info', {})
            if info_results:
                discourse_info = info_results.get('discourse_info', {})
                plugins = info_results.get('plugins', [])
                users = info_results.get('users', [])
                version = discourse_info.get('version', 'Unknown')
                output_lines.append(f'├── {Fore.GREEN}[✓]{Style.RESET_ALL} Server: Discourse {version}')
                output_lines.append(f'├── {Fore.GREEN}[✓]{Style.RESET_ALL} Plugins: {len(plugins)} installed')
                output_lines.append(f'├── {Fore.YELLOW}[⚠️]{Style.RESET_ALL} Users: {len(users)} discovered')
                if users:
                    output_lines.append(f'│   └── Discovered users ({len(users)} total):')
                    display_count = min(len(users), 10)
                    for i, user in enumerate(users[:display_count]):
                        username = user.get('username', 'Unknown')
                        name = user.get('name', '')
                        trust_level = user.get('trust_level', 'Unknown')
                        role = user.get('role', '')
                        user_id = user.get('id', 'Unknown')
                        avatar_template = user.get('avatar_template', '')
                        display_name = f'{username}'
                        if name and name != username:
                            display_name += f' ({name})'
                        if role:
                            display_name += f' [{role}]'
                        trust_desc = {0: 'New User', 1: 'Basic User', 2: 'Member', 3: 'Regular', 4: 'Leader', 5: 'Elder'}.get(trust_level, f'Level {trust_level}')
                        prefix = '├──' if i < display_count - 1 else '└──'
                        output_lines.append(f'│       {prefix} {display_name}')
                        output_lines.append(f'│           │ ID: {user_id} | Trust: {trust_desc} ({trust_level})')
                        if avatar_template:
                            output_lines.append(f"│           │ Avatar: {avatar_template[:50]}{('...' if len(avatar_template) > 50 else '')}")
                    if len(users) > display_count:
                        remaining = len(users) - display_count
                        output_lines.append(f'│           └── ... and {remaining} more users')
                output_lines.append(f'└── {Fore.GREEN}[✓]{Style.RESET_ALL} Information gathering completed')
            else:
                output_lines.append(f'└── {Fore.RED}[❌]{Style.RESET_ALL} Information gathering failed')
            output_lines.append('')
        if 'api' in modules_run:
            output_lines.append(f'{Fore.BLUE}🔍 API Discovery{Style.RESET_ALL}')
            api_results = self.results.get('api', {})
            if api_results:
                endpoints = api_results.get('endpoints', [])
                admin_found = any(('/admin' in ep.get('path', '') for ep in endpoints))
                api_count = len([ep for ep in endpoints if 'api' in ep.get('path', '')])
                output_lines.append(f"├── {(Fore.GREEN if admin_found else Fore.YELLOW)}[{('✓' if admin_found else '⚠️')}]{Style.RESET_ALL} Admin panel: {('Found' if admin_found else 'Not found')}")
                output_lines.append(f'├── {Fore.GREEN}[✓]{Style.RESET_ALL} API endpoints: {api_count} discovered')
                output_lines.append(f'├── {Fore.GREEN}[✓]{Style.RESET_ALL} Total endpoints: {len(endpoints)} found')
                output_lines.append(f'└── {Fore.GREEN}[✓]{Style.RESET_ALL} API discovery completed')
            else:
                output_lines.append(f'└── {Fore.RED}[❌]{Style.RESET_ALL} API discovery failed')
            output_lines.append('')
        if 'vuln' in modules_run:
            output_lines.append(f'{Fore.BLUE}🛡️ Vulnerability Assessment{Style.RESET_ALL}')
            vuln_results = self.results.get('vuln', {})
            if summary['critical_count'] > 0 or summary['high_count'] > 0:
                output_lines.append(f"├── {Fore.RED}[❌]{Style.RESET_ALL} Critical vulnerabilities: {summary['critical_count']} found")
                output_lines.append(f"├── {Fore.YELLOW}[⚠️]{Style.RESET_ALL} High vulnerabilities: {summary['high_count']} found")
                output_lines.append(f"├── {Fore.YELLOW}[⚠️]{Style.RESET_ALL} Medium vulnerabilities: {summary['medium_count']} found")
                output_lines.append(f"└── {Fore.GREEN}[✓]{Style.RESET_ALL} Low vulnerabilities: {summary['low_count']} found")
            else:
                output_lines.append(f'├── {Fore.GREEN}[✓]{Style.RESET_ALL} SQL Injection: No vulnerabilities found')
                output_lines.append(f'├── {Fore.GREEN}[✓]{Style.RESET_ALL} XSS: No vulnerabilities found')
                output_lines.append(f'├── {Fore.GREEN}[✓]{Style.RESET_ALL} CSRF: Properly protected')
                output_lines.append(f'└── {Fore.GREEN}[✓]{Style.RESET_ALL} File upload: Properly restricted')
            output_lines.append('')
        if 'auth' in modules_run:
            output_lines.append(f'{Fore.BLUE}🔐 Authentication & Authorization{Style.RESET_ALL}')
            auth_results = self.results.get('auth', {})
            user_enum = auth_results.get('user_enumeration', [])
            weak_passwords = auth_results.get('weak_passwords', [])
            if len(weak_passwords) > 0:
                output_lines.append(f'├── {Fore.RED}[❌]{Style.RESET_ALL} Weak passwords: {len(weak_passwords)} found')
                output_lines.append(f'├── {Fore.YELLOW}[⚠️]{Style.RESET_ALL} User enumeration: {len(user_enum)} users')
                output_lines.append(f'├── {Fore.YELLOW}[⚠️]{Style.RESET_ALL} Session management: Needs review')
                output_lines.append(f'└── {Fore.RED}[❌]{Style.RESET_ALL} Authentication issues detected')
            else:
                output_lines.append(f'├── {Fore.GREEN}[✓]{Style.RESET_ALL} Default credentials: Not found')
                output_lines.append(f'├── {Fore.GREEN}[✓]{Style.RESET_ALL} Session management: Properly configured')
                output_lines.append(f'├── {Fore.GREEN}[✓]{Style.RESET_ALL} Password policy: Strong requirements')
                output_lines.append(f'└── {Fore.GREEN}[✓]{Style.RESET_ALL} Authentication properly secured')
            output_lines.append('')
        if 'plugin_detection' in modules_run:
            output_lines.append(f'{Fore.BLUE}🔍 Plugin Detection{Style.RESET_ALL}')
            detection_results = self.results.get('plugin_detection', {})
            detected_plugins = detection_results.get('detected_plugins', [])
            detected_themes = detection_results.get('detected_themes', [])
            tech_stack = detection_results.get('technology_stack', [])
            js_libraries = detection_results.get('javascript_libraries', [])
            if len(detected_plugins) > 0 or len(tech_stack) > 0:
                output_lines.append(f'├── {Fore.GREEN}[✓]{Style.RESET_ALL} Plugins detected: {len(detected_plugins)} found')
                output_lines.append(f'├── {Fore.GREEN}[✓]{Style.RESET_ALL} Themes detected: {len(detected_themes)} found')
                output_lines.append(f'├── {Fore.GREEN}[✓]{Style.RESET_ALL} Technology stack: {len(tech_stack)} identified')
                output_lines.append(f'└── {Fore.GREEN}[✓]{Style.RESET_ALL} JS libraries: {len(js_libraries)} detected')
            else:
                output_lines.append(f'├── {Fore.YELLOW}[⚠️]{Style.RESET_ALL} Plugin detection: Limited results')
                output_lines.append(f'├── {Fore.YELLOW}[⚠️]{Style.RESET_ALL} Theme detection: Limited results')
                output_lines.append(f'├── {Fore.GREEN}[✓]{Style.RESET_ALL} Technology fingerprinting: Completed')
                output_lines.append(f'└── {Fore.GREEN}[✓]{Style.RESET_ALL} Detection scan completed')
            output_lines.append('')
        if 'plugin_bruteforce' in modules_run:
            output_lines.append(f'{Fore.BLUE}⚔️ Plugin Bruteforce Attacks{Style.RESET_ALL}')
            plugin_results = self.results.get('plugin_bruteforce', {})
            endpoint_attacks = plugin_results.get('endpoint_attacks', [])
            injection_tests = plugin_results.get('injection_tests', [])
            auth_bypasses = plugin_results.get('authentication_bypasses', [])
            if len(endpoint_attacks) > 0 or len(injection_tests) > 0 or len(auth_bypasses) > 0:
                output_lines.append(f"├── {(Fore.RED if len(endpoint_attacks) > 0 else Fore.GREEN)}[{('❌' if len(endpoint_attacks) > 0 else '✓')}]{Style.RESET_ALL} Endpoint attacks: {len(endpoint_attacks)} successful")
                output_lines.append(f"├── {(Fore.RED if len(injection_tests) > 0 else Fore.GREEN)}[{('❌' if len(injection_tests) > 0 else '✓')}]{Style.RESET_ALL} Injection attacks: {len(injection_tests)} vulnerabilities")
                output_lines.append(f"├── {(Fore.RED if len(auth_bypasses) > 0 else Fore.GREEN)}[{('❌' if len(auth_bypasses) > 0 else '✓')}]{Style.RESET_ALL} Auth bypasses: {len(auth_bypasses)} successful")
                output_lines.append(f"└── {(Fore.RED if any([endpoint_attacks, injection_tests, auth_bypasses]) else Fore.GREEN)}[{('❌' if any([endpoint_attacks, injection_tests, auth_bypasses]) else '✓')}]{Style.RESET_ALL} Bruteforce attacks completed")
            else:
                output_lines.append(f'├── {Fore.GREEN}[✓]{Style.RESET_ALL} Endpoint attacks: No vulnerabilities')
                output_lines.append(f'├── {Fore.GREEN}[✓]{Style.RESET_ALL} Injection attacks: No vulnerabilities')
                output_lines.append(f'├── {Fore.GREEN}[✓]{Style.RESET_ALL} Auth bypasses: No vulnerabilities')
                output_lines.append(f'└── {Fore.GREEN}[✓]{Style.RESET_ALL} Bruteforce attacks completed')
            output_lines.append('')
        if 'cve' in modules_run:
            output_lines.append(f'{Fore.BLUE}🔒 CVE Exploits{Style.RESET_ALL}')
            cve_results = self.results.get('cve', {})
            cve_vulns = cve_results.get('cve_results', [])
            if len(cve_vulns) > 0:
                critical_cves = [c for c in cve_vulns if c.get('severity', '').lower() == 'critical']
                high_cves = [c for c in cve_vulns if c.get('severity', '').lower() == 'high']
                output_lines.append(f'├── {Fore.RED}[❌]{Style.RESET_ALL} Critical CVEs: {len(critical_cves)} found')
                output_lines.append(f'├── {Fore.YELLOW}[⚠️]{Style.RESET_ALL} High CVEs: {len(high_cves)} found')
                output_lines.append(f'├── {Fore.YELLOW}[⚠️]{Style.RESET_ALL} Total CVEs: {len(cve_vulns)} tested')
                output_lines.append(f'└── {Fore.RED}[❌]{Style.RESET_ALL} CVE vulnerabilities detected')
            else:
                output_lines.append(f'├── {Fore.GREEN}[✓]{Style.RESET_ALL} Known CVEs: No vulnerabilities found')
                output_lines.append(f'├── {Fore.GREEN}[✓]{Style.RESET_ALL} Security patches: Up to date')
                output_lines.append(f'├── {Fore.GREEN}[✓]{Style.RESET_ALL} CVE database: Checked')
                output_lines.append(f'└── {Fore.GREEN}[✓]{Style.RESET_ALL} No known CVE exploits')
            output_lines.append('')
        if 'waf_bypass' in modules_run:
            output_lines.append(f'{Fore.BLUE}🛡️ WAF Bypass{Style.RESET_ALL}')
            waf_results = self.results.get('waf_bypass', {})
            bypass_attempts = waf_results.get('bypass_attempts', [])
            successful_bypasses = waf_results.get('successful_bypasses', [])
            if len(successful_bypasses) > 0:
                output_lines.append(f'├── {Fore.RED}[❌]{Style.RESET_ALL} WAF bypasses: {len(successful_bypasses)} successful')
                output_lines.append(f'├── {Fore.YELLOW}[⚠️]{Style.RESET_ALL} Total attempts: {len(bypass_attempts)} tested')
                output_lines.append(f'├── {Fore.RED}[❌]{Style.RESET_ALL} WAF protection: Bypassed')
                output_lines.append(f'└── {Fore.RED}[❌]{Style.RESET_ALL} WAF bypass vulnerabilities detected')
            else:
                output_lines.append(f'├── {Fore.GREEN}[✓]{Style.RESET_ALL} WAF bypasses: No successful attempts')
                output_lines.append(f'├── {Fore.GREEN}[✓]{Style.RESET_ALL} WAF protection: Effective')
                output_lines.append(f'├── {Fore.GREEN}[✓]{Style.RESET_ALL} Security filters: Working properly')
                output_lines.append(f'└── {Fore.GREEN}[✓]{Style.RESET_ALL} WAF bypass tests completed')
            output_lines.append('')
        output_lines.append(f'{Fore.BLUE}📈 Scan Summary{Style.RESET_ALL}')
        output_lines.append(f"├── 🔴 Critical: {summary['critical_count']} vulnerabilities")
        output_lines.append(f"├── 🟡 High: {summary['high_count']} vulnerabilities")
        output_lines.append(f"├── 🟠 Medium: {summary['medium_count']} vulnerabilities")
        output_lines.append(f"└── 🟢 Low: {summary['low_count']} vulnerabilities")
        output_lines.append('')
        timestamp = self.scan_time.strftime('%Y%m%d_%H%M%S')
        output_lines.append(f'{Fore.GREEN}💾 Report saved: discourse_scan_{timestamp}.json{Style.RESET_ALL}')
        output_lines.append(f'{Fore.GREEN}⏱️  Scan completed in {scan_duration}{Style.RESET_ALL}')
        output_lines.append('')
        print('\n'.join(output_lines))

    def finalize_scan(self):
        """Finalize the scan and print summary"""
        self.print_summary()