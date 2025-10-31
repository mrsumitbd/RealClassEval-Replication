import pytest
import snippet_320 as module_0

def test_case_0():
    str_0 = ']NOFY9p+g|v\x0b*&?I'
    none_type_0 = None
    workflow_state_0 = module_0.WorkflowState(str_0, str_0, str_0, none_type_0, none_type_0, none_type_0)
    assert f'{type(workflow_state_0).__module__}.{type(workflow_state_0).__qualname__}' == 'snippet_320.WorkflowState'
    assert workflow_state_0.workflow_id == ']NOFY9p+g|v\x0b*&?I'
    assert workflow_state_0.current_step_id == ']NOFY9p+g|v\x0b*&?I'
    assert workflow_state_0.step_history == ']NOFY9p+g|v\x0b*&?I'
    assert workflow_state_0.responses is None
    assert workflow_state_0.metadata is None
    assert workflow_state_0.created_at is None
    assert f'{type(workflow_state_0.updated_at).__module__}.{type(workflow_state_0.updated_at).__qualname__}' == 'datetime.datetime'

def test_case_1():
    none_type_0 = None
    str_0 = ''
    workflow_state_0 = module_0.WorkflowState(none_type_0, str_0, created_at=str_0, updated_at=none_type_0)
    assert f'{type(workflow_state_0).__module__}.{type(workflow_state_0).__qualname__}' == 'snippet_320.WorkflowState'
    assert workflow_state_0.workflow_id is None
    assert workflow_state_0.current_step_id == ''
    assert workflow_state_0.step_history == ['']
    assert workflow_state_0.responses == {}
    assert workflow_state_0.metadata == {}
    assert workflow_state_0.created_at == ''
    assert workflow_state_0.updated_at is None

def test_case_2():
    none_type_0 = None
    dict_0 = {none_type_0: none_type_0}
    str_0 = '59 D</)\x0b\t;HJn:jKOsig'
    str_1 = '{tb&70h*)fi$d) RW}\n'
    workflow_state_0 = module_0.WorkflowState(none_type_0, str_1, created_at=str_0)
    assert f'{type(workflow_state_0).__module__}.{type(workflow_state_0).__qualname__}' == 'snippet_320.WorkflowState'
    assert workflow_state_0.workflow_id is None
    assert workflow_state_0.current_step_id == '{tb&70h*)fi$d) RW}\n'
    assert workflow_state_0.step_history == ['{tb&70h*)fi$d) RW}\n']
    assert workflow_state_0.responses == {}
    assert workflow_state_0.metadata == {}
    assert workflow_state_0.created_at == '59 D</)\x0b\t;HJn:jKOsig'
    assert f'{type(workflow_state_0.updated_at).__module__}.{type(workflow_state_0.updated_at).__qualname__}' == 'datetime.datetime'
    var_0 = workflow_state_0.add_response(none_type_0, str_0)
    assert workflow_state_0.responses == {None: '59 D</)\x0b\t;HJn:jKOsig'}
    str_2 = ''
    str_3 = 'rtY\x0c8&5p..qkt1\rk mo'
    list_0 = [str_0, str_3]
    workflow_state_1 = module_0.WorkflowState(dict_0, str_2, list_0, created_at=list_0)
    assert f'{type(workflow_state_1).__module__}.{type(workflow_state_1).__qualname__}' == 'snippet_320.WorkflowState'
    assert workflow_state_1.workflow_id == {None: None}
    assert workflow_state_1.current_step_id == ''
    assert workflow_state_1.step_history == ['59 D</)\x0b\t;HJn:jKOsig', 'rtY\x0c8&5p..qkt1\rk mo']
    assert workflow_state_1.responses == {}
    assert workflow_state_1.metadata == {}
    assert workflow_state_1.created_at == ['59 D</)\x0b\t;HJn:jKOsig', 'rtY\x0c8&5p..qkt1\rk mo']
    assert f'{type(workflow_state_1.updated_at).__module__}.{type(workflow_state_1.updated_at).__qualname__}' == 'datetime.datetime'
    var_1 = workflow_state_1.go_back()
    assert var_1 == '59 D</)\x0b\t;HJn:jKOsig'
    assert workflow_state_1.current_step_id == '59 D</)\x0b\t;HJn:jKOsig'
    assert workflow_state_1.step_history == ['59 D</)\x0b\t;HJn:jKOsig']
    assert workflow_state_1.created_at == ['59 D</)\x0b\t;HJn:jKOsig']

def test_case_3():
    str_0 = ''
    str_1 = '>M*z16tqqT<J'
    str_2 = '[GP`S\x0c@\t).p`4`5/nd'
    dict_0 = {str_1: str_0, str_2: str_1}
    str_3 = 'Hp\\\x0c6q.Q|)\t\tKV0\n'
    workflow_state_0 = module_0.WorkflowState(str_1, str_3, metadata=dict_0)
    assert f'{type(workflow_state_0).__module__}.{type(workflow_state_0).__qualname__}' == 'snippet_320.WorkflowState'
    assert workflow_state_0.workflow_id == '>M*z16tqqT<J'
    assert workflow_state_0.current_step_id == 'Hp\\\x0c6q.Q|)\t\tKV0\n'
    assert workflow_state_0.step_history == ['Hp\\\x0c6q.Q|)\t\tKV0\n']
    assert workflow_state_0.responses == {}
    assert workflow_state_0.metadata == {'>M*z16tqqT<J': '', '[GP`S\x0c@\t).p`4`5/nd': '>M*z16tqqT<J'}
    assert f'{type(workflow_state_0.created_at).__module__}.{type(workflow_state_0.created_at).__qualname__}' == 'datetime.datetime'
    assert f'{type(workflow_state_0.updated_at).__module__}.{type(workflow_state_0.updated_at).__qualname__}' == 'datetime.datetime'
    workflow_state_0.get_all_responses()
    workflow_state_0.go_back()

def test_case_4():
    str_0 = '|p^hpp^S7X'
    str_1 = ''
    str_2 = '*kb\\]>R5i|'
    str_3 = '37u'
    dict_0 = {str_1: str_1, str_2: str_2, str_2: str_3, str_0: str_3}
    workflow_state_0 = module_0.WorkflowState(str_0, str_1, metadata=dict_0)
    assert f'{type(workflow_state_0).__module__}.{type(workflow_state_0).__qualname__}' == 'snippet_320.WorkflowState'
    assert workflow_state_0.workflow_id == '|p^hpp^S7X'
    assert workflow_state_0.current_step_id == ''
    assert workflow_state_0.step_history == ['']
    assert workflow_state_0.responses == {}
    assert workflow_state_0.metadata == {'': '', '*kb\\]>R5i|': '37u', '|p^hpp^S7X': '37u'}
    assert f'{type(workflow_state_0.created_at).__module__}.{type(workflow_state_0.created_at).__qualname__}' == 'datetime.datetime'
    assert f'{type(workflow_state_0.updated_at).__module__}.{type(workflow_state_0.updated_at).__qualname__}' == 'datetime.datetime'

def test_case_5():
    str_0 = ''
    str_1 = '>M*z16tqqT<J'
    dict_0 = {str_1: str_0, str_0: str_1}
    str_2 = 'Hp\\\x0c6q.Q|)\t\tKV0\n'
    workflow_state_0 = module_0.WorkflowState(str_1, str_2, metadata=dict_0)
    assert f'{type(workflow_state_0).__module__}.{type(workflow_state_0).__qualname__}' == 'snippet_320.WorkflowState'
    assert workflow_state_0.workflow_id == '>M*z16tqqT<J'
    assert workflow_state_0.current_step_id == 'Hp\\\x0c6q.Q|)\t\tKV0\n'
    assert workflow_state_0.step_history == ['Hp\\\x0c6q.Q|)\t\tKV0\n']
    assert workflow_state_0.responses == {}
    assert workflow_state_0.metadata == {'>M*z16tqqT<J': '', '': '>M*z16tqqT<J'}
    assert f'{type(workflow_state_0.created_at).__module__}.{type(workflow_state_0.created_at).__qualname__}' == 'datetime.datetime'
    assert f'{type(workflow_state_0.updated_at).__module__}.{type(workflow_state_0.updated_at).__qualname__}' == 'datetime.datetime'
    workflow_state_0.get_all_responses()
    var_0 = workflow_state_0.add_response(str_0, dict_0)
    assert workflow_state_0.responses == {'': {'>M*z16tqqT<J': '', '': '>M*z16tqqT<J'}}

@pytest.mark.xfail(strict=True)
def test_case_6():
    int_0 = 793
    str_0 = ''
    str_1 = '>M*z16tqqT<J'
    str_2 = '[GP`S\x0c@\t).p`4`5/nd'
    dict_0 = {str_1: str_0, str_2: str_1}
    str_3 = '#3'
    str_4 = '^r'
    workflow_state_0 = module_0.WorkflowState(str_1, int_0, metadata=dict_0)
    assert f'{type(workflow_state_0).__module__}.{type(workflow_state_0).__qualname__}' == 'snippet_320.WorkflowState'
    assert workflow_state_0.workflow_id == '>M*z16tqqT<J'
    assert workflow_state_0.current_step_id == 793
    assert workflow_state_0.step_history == [793]
    assert workflow_state_0.responses == {}
    assert workflow_state_0.metadata == {'>M*z16tqqT<J': '', '[GP`S\x0c@\t).p`4`5/nd': '>M*z16tqqT<J'}
    assert f'{type(workflow_state_0.created_at).__module__}.{type(workflow_state_0.created_at).__qualname__}' == 'datetime.datetime'
    assert f'{type(workflow_state_0.updated_at).__module__}.{type(workflow_state_0.updated_at).__qualname__}' == 'datetime.datetime'
    workflow_state_0.get_all_responses()
    str_5 = 'gDUE4LqyD'
    list_0 = [str_3, str_4, str_5]
    workflow_state_1 = module_0.WorkflowState(str_1, str_2, list_0, dict_0, str_5)
    assert f'{type(workflow_state_1).__module__}.{type(workflow_state_1).__qualname__}' == 'snippet_320.WorkflowState'
    assert workflow_state_1.workflow_id == '>M*z16tqqT<J'
    assert workflow_state_1.current_step_id == '[GP`S\x0c@\t).p`4`5/nd'
    assert workflow_state_1.step_history == ['#3', '^r', 'gDUE4LqyD']
    assert workflow_state_1.responses == {'>M*z16tqqT<J': '', '[GP`S\x0c@\t).p`4`5/nd': '>M*z16tqqT<J'}
    assert workflow_state_1.metadata == 'gDUE4LqyD'
    assert f'{type(workflow_state_1.created_at).__module__}.{type(workflow_state_1.created_at).__qualname__}' == 'datetime.datetime'
    assert f'{type(workflow_state_1.updated_at).__module__}.{type(workflow_state_1.updated_at).__qualname__}' == 'datetime.datetime'
    workflow_state_1.get_all_responses()

def test_case_7():
    int_0 = 793
    str_0 = ''
    str_1 = '>M*z16tqqT<J'
    str_2 = '[GP`S\x0c@\t).p`4`5/nd'
    dict_0 = {str_1: str_0, str_2: str_1}
    str_3 = 'Hp\\\x0c6q.Q|)\t\tKV0\n'
    workflow_state_0 = module_0.WorkflowState(str_1, str_3, metadata=dict_0)
    assert f'{type(workflow_state_0).__module__}.{type(workflow_state_0).__qualname__}' == 'snippet_320.WorkflowState'
    assert workflow_state_0.workflow_id == '>M*z16tqqT<J'
    assert workflow_state_0.current_step_id == 'Hp\\\x0c6q.Q|)\t\tKV0\n'
    assert workflow_state_0.step_history == ['Hp\\\x0c6q.Q|)\t\tKV0\n']
    assert workflow_state_0.responses == {}
    assert workflow_state_0.metadata == {'>M*z16tqqT<J': '', '[GP`S\x0c@\t).p`4`5/nd': '>M*z16tqqT<J'}
    assert f'{type(workflow_state_0.created_at).__module__}.{type(workflow_state_0.created_at).__qualname__}' == 'datetime.datetime'
    assert f'{type(workflow_state_0.updated_at).__module__}.{type(workflow_state_0.updated_at).__qualname__}' == 'datetime.datetime'
    var_0 = workflow_state_0.add_response(int_0, dict_0)
    assert workflow_state_0.responses == {793: {'>M*z16tqqT<J': '', '[GP`S\x0c@\t).p`4`5/nd': '>M*z16tqqT<J'}}
    workflow_state_0.go_back()
    str_4 = 'N'
    dict_1 = workflow_state_0.get_all_responses()
    workflow_state_1 = module_0.WorkflowState(str_1, str_2, dict_1, dict_0, str_4)
    assert f'{type(workflow_state_1).__module__}.{type(workflow_state_1).__qualname__}' == 'snippet_320.WorkflowState'
    assert workflow_state_1.workflow_id == '>M*z16tqqT<J'
    assert workflow_state_1.current_step_id == '[GP`S\x0c@\t).p`4`5/nd'
    assert workflow_state_1.step_history == {'793.>M*z16tqqT<J': '', '>M*z16tqqT<J': '', '793.[GP`S\x0c@\t).p`4`5/nd': '>M*z16tqqT<J', '[GP`S\x0c@\t).p`4`5/nd': '>M*z16tqqT<J'}
    assert workflow_state_1.responses == {'>M*z16tqqT<J': '', '[GP`S\x0c@\t).p`4`5/nd': '>M*z16tqqT<J'}
    assert workflow_state_1.metadata == 'N'
    assert f'{type(workflow_state_1.created_at).__module__}.{type(workflow_state_1.created_at).__qualname__}' == 'datetime.datetime'
    assert f'{type(workflow_state_1.updated_at).__module__}.{type(workflow_state_1.updated_at).__qualname__}' == 'datetime.datetime'