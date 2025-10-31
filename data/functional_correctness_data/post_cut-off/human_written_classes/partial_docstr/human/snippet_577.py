import re

class MaliciousPatternChecker:
    """Utility class for detecting malicious patterns in content"""

    def __init__(self):
        self.malicious_patterns = ['eval\\s*\\(', 'exec\\s*\\(', 'system\\s*\\(', 'shell_exec\\s*\\(', 'passthru\\s*\\(', 'base64_decode\\s*\\(', 'gzinflate\\s*\\(', 'str_rot13\\s*\\(', '\\$_GET\\s*\\[', '\\$_POST\\s*\\[', '\\$_REQUEST\\s*\\[', 'file_get_contents\\s*\\(', 'fopen\\s*\\(', 'fwrite\\s*\\(', 'curl_exec\\s*\\(', 'wget\\s+', 'nc\\s+-', '/bin/sh', '/bin/bash']
        self.suspicious_js_patterns = ['document\\.write\\s*\\(', 'innerHTML\\s*=', 'eval\\s*\\(', 'setTimeout\\s*\\(', 'setInterval\\s*\\(', 'XMLHttpRequest\\s*\\(', 'fetch\\s*\\(', 'window\\.location', 'document\\.cookie', 'localStorage', 'sessionStorage']
        self.suspicious_js_indicators = ['eval(', 'document.write(', 'unescape(', 'String.fromCharCode(', 'atob(', 'btoa(', 'setTimeout(', 'setInterval(']

    def check_malicious_patterns(self, content):
        """Check content for malicious patterns"""
        found_patterns = []
        for pattern in self.malicious_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                found_patterns.append(pattern)
        return found_patterns

    def check_suspicious_plugin_content(self, content):
        """Check plugin content for suspicious patterns"""
        found_patterns = []
        for pattern in self.suspicious_js_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                found_patterns.append(pattern)
        return found_patterns

    def has_suspicious_js_content(self, content):
        """Check if JavaScript content has suspicious characteristics"""
        count = sum((1 for indicator in self.suspicious_js_indicators if indicator in content))
        return count > 3