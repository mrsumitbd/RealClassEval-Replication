import pytest
import snippet_62 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    read_write_lock_0 = module_0.ReadWriteLock()
    assert f'{type(read_write_lock_0).__module__}.{type(read_write_lock_0).__qualname__}' == 'snippet_62.ReadWriteLock'
    read_write_lock_0.acquire_read()
    read_write_lock_1 = module_0.ReadWriteLock()
    assert f'{type(read_write_lock_1).__module__}.{type(read_write_lock_1).__qualname__}' == 'snippet_62.ReadWriteLock'
    read_write_lock_1.acquire_read(timeout=read_write_lock_0)

def test_case_1():
    read_write_lock_0 = module_0.ReadWriteLock()
    assert f'{type(read_write_lock_0).__module__}.{type(read_write_lock_0).__qualname__}' == 'snippet_62.ReadWriteLock'
    read_write_lock_0.acquire_read()

def test_case_2():
    read_write_lock_0 = module_0.ReadWriteLock()
    assert f'{type(read_write_lock_0).__module__}.{type(read_write_lock_0).__qualname__}' == 'snippet_62.ReadWriteLock'
    read_write_lock_0.acquire_read()
    read_write_lock_0.acquire_write()
    read_write_lock_0.acquire_read()

@pytest.mark.xfail(strict=True)
def test_case_3():
    read_write_lock_0 = module_0.ReadWriteLock()
    assert f'{type(read_write_lock_0).__module__}.{type(read_write_lock_0).__qualname__}' == 'snippet_62.ReadWriteLock'
    read_write_lock_0.acquire_write(timeout=read_write_lock_0)

def test_case_4():
    read_write_lock_0 = module_0.ReadWriteLock()
    assert f'{type(read_write_lock_0).__module__}.{type(read_write_lock_0).__qualname__}' == 'snippet_62.ReadWriteLock'
    read_write_lock_0.acquire_write()

def test_case_5():
    read_write_lock_0 = module_0.ReadWriteLock()
    assert f'{type(read_write_lock_0).__module__}.{type(read_write_lock_0).__qualname__}' == 'snippet_62.ReadWriteLock'
    read_write_lock_0.acquire_read()
    read_write_lock_0.acquire_write()
    read_write_lock_0.acquire_write()

def test_case_6():
    read_write_lock_0 = module_0.ReadWriteLock()
    assert f'{type(read_write_lock_0).__module__}.{type(read_write_lock_0).__qualname__}' == 'snippet_62.ReadWriteLock'
    read_write_lock_0.acquire_read()
    read_write_lock_0.acquire_write()
    read_write_lock_0.release()

def test_case_7():
    read_write_lock_0 = module_0.ReadWriteLock()
    assert f'{type(read_write_lock_0).__module__}.{type(read_write_lock_0).__qualname__}' == 'snippet_62.ReadWriteLock'
    with pytest.raises(ValueError):
        read_write_lock_0.release()

def test_case_8():
    read_write_lock_0 = module_0.ReadWriteLock()
    assert f'{type(read_write_lock_0).__module__}.{type(read_write_lock_0).__qualname__}' == 'snippet_62.ReadWriteLock'

def test_case_9():
    read_write_lock_0 = module_0.ReadWriteLock()
    assert f'{type(read_write_lock_0).__module__}.{type(read_write_lock_0).__qualname__}' == 'snippet_62.ReadWriteLock'
    read_write_lock_0.acquire_read()
    read_write_lock_0.acquire_write()

def test_case_10():
    read_write_lock_0 = module_0.ReadWriteLock()
    assert f'{type(read_write_lock_0).__module__}.{type(read_write_lock_0).__qualname__}' == 'snippet_62.ReadWriteLock'
    read_write_lock_0.acquire_write()
    read_write_lock_1 = module_0.ReadWriteLock()
    assert f'{type(read_write_lock_1).__module__}.{type(read_write_lock_1).__qualname__}' == 'snippet_62.ReadWriteLock'
    read_write_lock_0.release()
    with pytest.raises(ValueError):
        read_write_lock_1.release()

def test_case_11():
    read_write_lock_0 = module_0.ReadWriteLock()
    assert f'{type(read_write_lock_0).__module__}.{type(read_write_lock_0).__qualname__}' == 'snippet_62.ReadWriteLock'
    read_write_lock_0.acquire_read()
    read_write_lock_0.release()

def test_case_12():
    read_write_lock_0 = module_0.ReadWriteLock()
    assert f'{type(read_write_lock_0).__module__}.{type(read_write_lock_0).__qualname__}' == 'snippet_62.ReadWriteLock'
    none_type_0 = None
    read_write_lock_0.acquire_write()
    read_write_lock_1 = module_0.ReadWriteLock()
    assert f'{type(read_write_lock_1).__module__}.{type(read_write_lock_1).__qualname__}' == 'snippet_62.ReadWriteLock'
    read_write_lock_1.acquire_read(timeout=none_type_0)
    read_write_lock_1.acquire_read()
    read_write_lock_1.release()