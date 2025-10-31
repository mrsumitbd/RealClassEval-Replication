from typing import Dict, Any, Optional, List, Set, Tuple
import re

class PromptPatternMatcher:
    """Analyzes prompts to determine context requirements."""

    def __init__(self):
        """Initialize pattern matchers."""
        self.patterns = {'incident': ['(?i)\\b(incident|attack|breach|compromise|intrusion)\\b', '(?i)\\b(investigate|investigation|forensic|what happened)\\b', '(?i)\\b(suspicious|malicious|threat|IOC)\\b', '(?i)\\b(timeline|sequence|chain of events)\\b'], 'hunting': ['(?i)\\b(hunt|hunting|search for|look for)\\b', '(?i)\\b(IOC|indicator|suspicious activity)\\b', '(?i)\\b(lateral movement|persistence|privilege escalation)\\b', '(?i)\\b(anomaly|unusual|abnormal|outlier)\\b'], 'compliance': ['(?i)\\b(compliance|audit|policy|regulation)\\b', '(?i)\\b(PCI|HIPAA|SOX|GDPR|CIS)\\b', '(?i)\\b(configuration|hardening|baseline)\\b', '(?i)\\b(violation|non-compliant|failed check)\\b'], 'forensic': ['(?i)\\b(forensic|evidence|artifact|trace)\\b', '(?i)\\b(log analysis|timeline|reconstruction)\\b', '(?i)\\b(root cause|attribution|analysis)\\b', '(?i)\\b(correlation|relationship|connection)\\b'], 'monitoring': ['(?i)\\b(monitor|monitoring|status|health)\\b', '(?i)\\b(dashboard|overview|summary)\\b', '(?i)\\b(performance|metrics|statistics)\\b', '(?i)\\b(trend|pattern|baseline)\\b']}
        self.entity_patterns = {'agent_id': '\\b([0-9a-fA-F]{3,8})\\b', 'ip_address': '\\b(?:[0-9]{1,3}\\.){3}[0-9]{1,3}\\b', 'hash': '\\b[a-fA-F0-9]{32,64}\\b', 'domain': '\\b[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}\\b', 'process_name': '\\b\\w+\\.exe\\b|\\b\\w+\\.bin\\b|\\b\\w+\\.sh\\b', 'port': '\\bport\\s+(\\d+)\\b|\\b:(\\d+)\\b'}

    def analyze_prompt(self, prompt: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze prompt to determine context requirements.

        Returns:
            Dictionary with detected patterns, entities, and confidence scores
        """
        analysis = {'context_types': {}, 'entities': {}, 'priority': 'medium', 'confidence': 0.0}
        for context_type, patterns in self.patterns.items():
            score = 0.0
            matches = []
            for pattern in patterns:
                found = re.findall(pattern, prompt)
                if found:
                    score += 1.0 / len(patterns)
                    matches.extend(found)
            if score > 0:
                analysis['context_types'][context_type] = {'score': score, 'matches': matches}
        for entity_type, pattern in self.entity_patterns.items():
            matches = re.findall(pattern, prompt)
            if matches:
                analysis['entities'][entity_type] = matches
        if 'agent_id' in arguments:
            analysis['entities']['agent_id'] = [arguments['agent_id']]
        priority_keywords = {'critical': ['critical', 'urgent', 'emergency', 'breach', 'compromise'], 'high': ['important', 'security', 'incident', 'attack', 'malicious'], 'medium': ['investigate', 'check', 'review', 'analyze'], 'low': ['status', 'summary', 'overview', 'general']}
        for priority, keywords in priority_keywords.items():
            for keyword in keywords:
                if re.search(f'\\b{keyword}\\b', prompt, re.IGNORECASE):
                    analysis['priority'] = priority
                    break
            if analysis['priority'] != 'medium':
                break
        if analysis['context_types']:
            max_score = max((ctx['score'] for ctx in analysis['context_types'].values()))
            analysis['confidence'] = min(max_score, 1.0)
        return analysis