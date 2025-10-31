import snippet_256 as module_0

def test_case_0():
    prompt_pattern_matcher_0 = module_0.PromptPatternMatcher()
    assert f'{type(prompt_pattern_matcher_0).__module__}.{type(prompt_pattern_matcher_0).__qualname__}' == 'snippet_256.PromptPatternMatcher'
    assert prompt_pattern_matcher_0.patterns == {'incident': ['(?i)\\b(incident|attack|breach|compromise|intrusion)\\b', '(?i)\\b(investigate|investigation|forensic|what happened)\\b', '(?i)\\b(suspicious|malicious|threat|IOC)\\b', '(?i)\\b(timeline|sequence|chain of events)\\b'], 'hunting': ['(?i)\\b(hunt|hunting|search for|look for)\\b', '(?i)\\b(IOC|indicator|suspicious activity)\\b', '(?i)\\b(lateral movement|persistence|privilege escalation)\\b', '(?i)\\b(anomaly|unusual|abnormal|outlier)\\b'], 'compliance': ['(?i)\\b(compliance|audit|policy|regulation)\\b', '(?i)\\b(PCI|HIPAA|SOX|GDPR|CIS)\\b', '(?i)\\b(configuration|hardening|baseline)\\b', '(?i)\\b(violation|non-compliant|failed check)\\b'], 'forensic': ['(?i)\\b(forensic|evidence|artifact|trace)\\b', '(?i)\\b(log analysis|timeline|reconstruction)\\b', '(?i)\\b(root cause|attribution|analysis)\\b', '(?i)\\b(correlation|relationship|connection)\\b'], 'monitoring': ['(?i)\\b(monitor|monitoring|status|health)\\b', '(?i)\\b(dashboard|overview|summary)\\b', '(?i)\\b(performance|metrics|statistics)\\b', '(?i)\\b(trend|pattern|baseline)\\b']}
    assert prompt_pattern_matcher_0.entity_patterns == {'agent_id': '\\b([0-9a-fA-F]{3,8})\\b', 'ip_address': '\\b(?:[0-9]{1,3}\\.){3}[0-9]{1,3}\\b', 'hash': '\\b[a-fA-F0-9]{32,64}\\b', 'domain': '\\b[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}\\b', 'process_name': '\\b\\w+\\.exe\\b|\\b\\w+\\.bin\\b|\\b\\w+\\.sh\\b', 'port': '\\bport\\s+(\\d+)\\b|\\b:(\\d+)\\b'}
    str_0 = ' eN\\\r'
    prompt_pattern_matcher_0.analyze_prompt(str_0, str_0, str_0)

def test_case_1():
    prompt_pattern_matcher_0 = module_0.PromptPatternMatcher()
    assert f'{type(prompt_pattern_matcher_0).__module__}.{type(prompt_pattern_matcher_0).__qualname__}' == 'snippet_256.PromptPatternMatcher'
    assert prompt_pattern_matcher_0.patterns == {'incident': ['(?i)\\b(incident|attack|breach|compromise|intrusion)\\b', '(?i)\\b(investigate|investigation|forensic|what happened)\\b', '(?i)\\b(suspicious|malicious|threat|IOC)\\b', '(?i)\\b(timeline|sequence|chain of events)\\b'], 'hunting': ['(?i)\\b(hunt|hunting|search for|look for)\\b', '(?i)\\b(IOC|indicator|suspicious activity)\\b', '(?i)\\b(lateral movement|persistence|privilege escalation)\\b', '(?i)\\b(anomaly|unusual|abnormal|outlier)\\b'], 'compliance': ['(?i)\\b(compliance|audit|policy|regulation)\\b', '(?i)\\b(PCI|HIPAA|SOX|GDPR|CIS)\\b', '(?i)\\b(configuration|hardening|baseline)\\b', '(?i)\\b(violation|non-compliant|failed check)\\b'], 'forensic': ['(?i)\\b(forensic|evidence|artifact|trace)\\b', '(?i)\\b(log analysis|timeline|reconstruction)\\b', '(?i)\\b(root cause|attribution|analysis)\\b', '(?i)\\b(correlation|relationship|connection)\\b'], 'monitoring': ['(?i)\\b(monitor|monitoring|status|health)\\b', '(?i)\\b(dashboard|overview|summary)\\b', '(?i)\\b(performance|metrics|statistics)\\b', '(?i)\\b(trend|pattern|baseline)\\b']}
    assert prompt_pattern_matcher_0.entity_patterns == {'agent_id': '\\b([0-9a-fA-F]{3,8})\\b', 'ip_address': '\\b(?:[0-9]{1,3}\\.){3}[0-9]{1,3}\\b', 'hash': '\\b[a-fA-F0-9]{32,64}\\b', 'domain': '\\b[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}\\b', 'process_name': '\\b\\w+\\.exe\\b|\\b\\w+\\.bin\\b|\\b\\w+\\.sh\\b', 'port': '\\bport\\s+(\\d+)\\b|\\b:(\\d+)\\b'}

def test_case_2():
    prompt_pattern_matcher_0 = module_0.PromptPatternMatcher()
    assert f'{type(prompt_pattern_matcher_0).__module__}.{type(prompt_pattern_matcher_0).__qualname__}' == 'snippet_256.PromptPatternMatcher'
    assert prompt_pattern_matcher_0.patterns == {'incident': ['(?i)\\b(incident|attack|breach|compromise|intrusion)\\b', '(?i)\\b(investigate|investigation|forensic|what happened)\\b', '(?i)\\b(suspicious|malicious|threat|IOC)\\b', '(?i)\\b(timeline|sequence|chain of events)\\b'], 'hunting': ['(?i)\\b(hunt|hunting|search for|look for)\\b', '(?i)\\b(IOC|indicator|suspicious activity)\\b', '(?i)\\b(lateral movement|persistence|privilege escalation)\\b', '(?i)\\b(anomaly|unusual|abnormal|outlier)\\b'], 'compliance': ['(?i)\\b(compliance|audit|policy|regulation)\\b', '(?i)\\b(PCI|HIPAA|SOX|GDPR|CIS)\\b', '(?i)\\b(configuration|hardening|baseline)\\b', '(?i)\\b(violation|non-compliant|failed check)\\b'], 'forensic': ['(?i)\\b(forensic|evidence|artifact|trace)\\b', '(?i)\\b(log analysis|timeline|reconstruction)\\b', '(?i)\\b(root cause|attribution|analysis)\\b', '(?i)\\b(correlation|relationship|connection)\\b'], 'monitoring': ['(?i)\\b(monitor|monitoring|status|health)\\b', '(?i)\\b(dashboard|overview|summary)\\b', '(?i)\\b(performance|metrics|statistics)\\b', '(?i)\\b(trend|pattern|baseline)\\b']}
    assert prompt_pattern_matcher_0.entity_patterns == {'agent_id': '\\b([0-9a-fA-F]{3,8})\\b', 'ip_address': '\\b(?:[0-9]{1,3}\\.){3}[0-9]{1,3}\\b', 'hash': '\\b[a-fA-F0-9]{32,64}\\b', 'domain': '\\b[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}\\b', 'process_name': '\\b\\w+\\.exe\\b|\\b\\w+\\.bin\\b|\\b\\w+\\.sh\\b', 'port': '\\bport\\s+(\\d+)\\b|\\b:(\\d+)\\b'}
    str_0 = ''
    str_1 = '$\\yb'
    int_0 = 2618
    str_2 = 'Ss[fG\\i"U'
    dict_0 = {str_0: prompt_pattern_matcher_0, str_1: prompt_pattern_matcher_0, str_0: int_0, str_2: prompt_pattern_matcher_0}
    dict_1 = prompt_pattern_matcher_0.analyze_prompt(str_0, str_0, dict_0)
    str_3 = 'S\t]%(=fFe\\56v'
    prompt_pattern_matcher_0.analyze_prompt(str_3, dict_1, str_3)