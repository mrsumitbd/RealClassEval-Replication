import snippet_240 as module_0

def test_case_0():
    external_issue_0 = module_0.ExternalIssue()
    assert f'{type(external_issue_0).__module__}.{type(external_issue_0).__qualname__}' == 'snippet_240.ExternalIssue'
    assert external_issue_0.bts_url is None
    assert external_issue_0.bts_project is None
    assert external_issue_0.submit_date is None
    assert external_issue_0.ticket_id is None
    assert external_issue_0.url is None
    assert f'{type(module_0.ExternalIssue.payload).__module__}.{type(module_0.ExternalIssue.payload).__qualname__}' == 'builtins.property'