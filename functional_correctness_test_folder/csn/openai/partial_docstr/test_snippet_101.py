import pytest
import snippet_101 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    closable_named_temporary_file_0 = module_0.ClosableNamedTemporaryFile()
    assert f'{type(closable_named_temporary_file_0).__module__}.{type(closable_named_temporary_file_0).__qualname__}' == 'snippet_101.ClosableNamedTemporaryFile'
    assert f'{type(closable_named_temporary_file_0.file).__module__}.{type(closable_named_temporary_file_0.file).__qualname__}' == 'tempfile._TemporaryFileWrapper'
    closable_named_temporary_file_0.__del__()
    closable_named_temporary_file_0.__del__()

def test_case_1():
    closable_named_temporary_file_0 = module_0.ClosableNamedTemporaryFile()
    assert f'{type(closable_named_temporary_file_0).__module__}.{type(closable_named_temporary_file_0).__qualname__}' == 'snippet_101.ClosableNamedTemporaryFile'
    assert f'{type(closable_named_temporary_file_0.file).__module__}.{type(closable_named_temporary_file_0.file).__qualname__}' == 'tempfile._TemporaryFileWrapper'

@pytest.mark.xfail(strict=True)
def test_case_2():
    bool_0 = False
    set_0 = {bool_0}
    closable_named_temporary_file_0 = module_0.ClosableNamedTemporaryFile()
    assert f'{type(closable_named_temporary_file_0).__module__}.{type(closable_named_temporary_file_0).__qualname__}' == 'snippet_101.ClosableNamedTemporaryFile'
    assert f'{type(closable_named_temporary_file_0.file).__module__}.{type(closable_named_temporary_file_0.file).__qualname__}' == 'tempfile._TemporaryFileWrapper'
    closable_named_temporary_file_0.write(set_0)

def test_case_3():
    closable_named_temporary_file_0 = module_0.ClosableNamedTemporaryFile()
    assert f'{type(closable_named_temporary_file_0).__module__}.{type(closable_named_temporary_file_0).__qualname__}' == 'snippet_101.ClosableNamedTemporaryFile'
    assert f'{type(closable_named_temporary_file_0.file).__module__}.{type(closable_named_temporary_file_0.file).__qualname__}' == 'tempfile._TemporaryFileWrapper'
    closable_named_temporary_file_0.close()