import pytest
import snippet_153 as module_0

def test_case_0():
    str_0 = '}Lz6_UE[L1\x0by^!"\x0bnu'
    conditional_tracker_0 = module_0.ConditionalTracker()
    assert f'{type(conditional_tracker_0).__module__}.{type(conditional_tracker_0).__qualname__}' == 'snippet_153.ConditionalTracker'
    assert conditional_tracker_0.conditional_stack == []
    assert conditional_tracker_0.conditional_branch_id == 0
    conditional_tracker_0.process_line(str_0, str_0)

def test_case_1():
    conditional_tracker_0 = module_0.ConditionalTracker()
    assert f'{type(conditional_tracker_0).__module__}.{type(conditional_tracker_0).__qualname__}' == 'snippet_153.ConditionalTracker'
    assert conditional_tracker_0.conditional_stack == []
    assert conditional_tracker_0.conditional_branch_id == 0
    bool_0 = conditional_tracker_0.are_mutually_exclusive(conditional_tracker_0, conditional_tracker_0)
    assert bool_0 is False
    none_type_0 = None
    bool_1 = conditional_tracker_0.are_mutually_exclusive(none_type_0, bool_0)
    assert bool_1 is False
    conditional_tracker_0.reset()

def test_case_2():
    conditional_tracker_0 = module_0.ConditionalTracker()
    assert f'{type(conditional_tracker_0).__module__}.{type(conditional_tracker_0).__qualname__}' == 'snippet_153.ConditionalTracker'
    assert conditional_tracker_0.conditional_stack == []
    assert conditional_tracker_0.conditional_branch_id == 0
    float_0 = 2808.53
    bytes_0 = b'\xb1*\xbd\x1b\xa6\x99'
    tuple_0 = (bytes_0, float_0, bytes_0)
    bool_0 = conditional_tracker_0.are_mutually_exclusive(tuple_0, bytes_0)
    assert bool_0 is True

def test_case_3():
    conditional_tracker_0 = module_0.ConditionalTracker()
    assert f'{type(conditional_tracker_0).__module__}.{type(conditional_tracker_0).__qualname__}' == 'snippet_153.ConditionalTracker'
    assert conditional_tracker_0.conditional_stack == []
    assert conditional_tracker_0.conditional_branch_id == 0

def test_case_4():
    conditional_tracker_0 = module_0.ConditionalTracker()
    assert f'{type(conditional_tracker_0).__module__}.{type(conditional_tracker_0).__qualname__}' == 'snippet_153.ConditionalTracker'
    assert conditional_tracker_0.conditional_stack == []
    assert conditional_tracker_0.conditional_branch_id == 0
    conditional_tracker_0.reset()

@pytest.mark.xfail(strict=True)
def test_case_5():
    conditional_tracker_0 = module_0.ConditionalTracker()
    assert f'{type(conditional_tracker_0).__module__}.{type(conditional_tracker_0).__qualname__}' == 'snippet_153.ConditionalTracker'
    assert conditional_tracker_0.conditional_stack == []
    assert conditional_tracker_0.conditional_branch_id == 0
    bytes_0 = b'\x9c.\xb8\x163c\x1f \x0e\xac\xf6\xa6\xf6\xa3\x9b/\x90'
    list_0 = [conditional_tracker_0]
    tuple_0 = (bytes_0, bytes_0, bytes_0, list_0)
    conditional_tracker_1 = module_0.ConditionalTracker()
    assert f'{type(conditional_tracker_1).__module__}.{type(conditional_tracker_1).__qualname__}' == 'snippet_153.ConditionalTracker'
    assert conditional_tracker_1.conditional_stack == []
    assert conditional_tracker_1.conditional_branch_id == 0
    conditional_tracker_1.are_mutually_exclusive(conditional_tracker_0, tuple_0)

def test_case_6():
    conditional_tracker_0 = module_0.ConditionalTracker()
    assert f'{type(conditional_tracker_0).__module__}.{type(conditional_tracker_0).__qualname__}' == 'snippet_153.ConditionalTracker'
    assert conditional_tracker_0.conditional_stack == []
    assert conditional_tracker_0.conditional_branch_id == 0
    none_type_0 = conditional_tracker_0.reset()
    dict_0 = {}
    int_0 = 3381
    tuple_0 = (dict_0, conditional_tracker_0, int_0)
    bool_0 = conditional_tracker_0.are_mutually_exclusive(tuple_0, none_type_0)
    assert bool_0 is False