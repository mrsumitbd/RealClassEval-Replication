import snippet_178 as module_0

def test_case_0():
    str_0 = 'K=nB'
    none_type_0 = None
    table_cell_0 = module_0.TableCell(str_0, none_type_0)
    assert f'{type(table_cell_0).__module__}.{type(table_cell_0).__qualname__}' == 'snippet_178.TableCell'
    assert f'{type(module_0.TableCell.alignment).__module__}.{type(module_0.TableCell.alignment).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.TableCell.kind).__module__}.{type(module_0.TableCell.kind).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.TableCell.value).__module__}.{type(module_0.TableCell.value).__qualname__}' == 'builtins.member_descriptor'

def test_case_1():
    str_0 = 'oAgDUE'
    none_type_0 = None
    table_cell_0 = module_0.TableCell(none_type_0, none_type_0)
    assert f'{type(table_cell_0).__module__}.{type(table_cell_0).__qualname__}' == 'snippet_178.TableCell'
    assert f'{type(module_0.TableCell.alignment).__module__}.{type(module_0.TableCell.alignment).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.TableCell.kind).__module__}.{type(module_0.TableCell.kind).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.TableCell.value).__module__}.{type(module_0.TableCell.value).__qualname__}' == 'builtins.member_descriptor'
    table_cell_1 = module_0.TableCell(str_0, str_0, alignment=str_0)
    assert f'{type(table_cell_1).__module__}.{type(table_cell_1).__qualname__}' == 'snippet_178.TableCell'
    str_1 = table_cell_1.__repr__()
    assert str_1 == "TableCell(kind='oAgDUE', value='oAgDUE', alignment='oAgDUE')"

def test_case_2():
    none_type_0 = None
    table_cell_0 = module_0.TableCell(none_type_0, none_type_0)
    assert f'{type(table_cell_0).__module__}.{type(table_cell_0).__qualname__}' == 'snippet_178.TableCell'
    assert f'{type(module_0.TableCell.alignment).__module__}.{type(module_0.TableCell.alignment).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.TableCell.kind).__module__}.{type(module_0.TableCell.kind).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.TableCell.value).__module__}.{type(module_0.TableCell.value).__qualname__}' == 'builtins.member_descriptor'
    str_0 = table_cell_0.__str__()
    assert str_0 == ''