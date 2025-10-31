import snippet_164 as module_0

def test_case_0():
    patch_obj_0 = module_0.patch_obj()
    assert f'{type(patch_obj_0).__module__}.{type(patch_obj_0).__qualname__}' == 'snippet_164.patch_obj'
    assert patch_obj_0.diffs == []
    assert patch_obj_0.start1 is None
    assert patch_obj_0.start2 is None
    assert patch_obj_0.length1 == 0
    assert patch_obj_0.length2 == 0
    var_0 = patch_obj_0.__str__()
    assert var_0 == '@@ -None,0 +None,0 @@\n'