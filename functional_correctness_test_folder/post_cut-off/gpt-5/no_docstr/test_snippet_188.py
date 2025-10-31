import snippet_188 as module_0

def test_case_0():
    str_0 = ''
    log_cleanup_manager_0 = module_0.LogCleanupManager(str_0)
    assert f'{type(log_cleanup_manager_0).__module__}.{type(log_cleanup_manager_0).__qualname__}' == 'snippet_188.LogCleanupManager'
    assert f'{type(log_cleanup_manager_0.log_dir).__module__}.{type(log_cleanup_manager_0.log_dir).__qualname__}' == 'pathlib.PosixPath'
    assert log_cleanup_manager_0.max_age_days == 30
    assert log_cleanup_manager_0.cleanup_interval_hours == 24
    assert log_cleanup_manager_0.cleanup_thread is None
    assert f'{type(log_cleanup_manager_0.stop_event).__module__}.{type(log_cleanup_manager_0.stop_event).__qualname__}' == 'threading.Event'
    assert log_cleanup_manager_0.logger is None
    var_0 = log_cleanup_manager_0.start_cleanup_scheduler()
    assert f'{type(log_cleanup_manager_0.cleanup_thread).__module__}.{type(log_cleanup_manager_0.cleanup_thread).__qualname__}' == 'threading.Thread'
    assert f'{type(log_cleanup_manager_0.logger).__module__}.{type(log_cleanup_manager_0.logger).__qualname__}' == 'logging.Logger'
    log_cleanup_manager_0.get_cleanup_stats()
    log_cleanup_manager_0.start_cleanup_scheduler()

def test_case_1():
    str_0 = ''
    log_cleanup_manager_0 = module_0.LogCleanupManager(str_0)
    assert f'{type(log_cleanup_manager_0).__module__}.{type(log_cleanup_manager_0).__qualname__}' == 'snippet_188.LogCleanupManager'
    assert f'{type(log_cleanup_manager_0.log_dir).__module__}.{type(log_cleanup_manager_0.log_dir).__qualname__}' == 'pathlib.PosixPath'
    assert log_cleanup_manager_0.max_age_days == 30
    assert log_cleanup_manager_0.cleanup_interval_hours == 24
    assert log_cleanup_manager_0.cleanup_thread is None
    assert f'{type(log_cleanup_manager_0.stop_event).__module__}.{type(log_cleanup_manager_0.stop_event).__qualname__}' == 'threading.Event'
    assert log_cleanup_manager_0.logger is None
    var_0 = log_cleanup_manager_0.start_cleanup_scheduler()
    assert f'{type(log_cleanup_manager_0.cleanup_thread).__module__}.{type(log_cleanup_manager_0.cleanup_thread).__qualname__}' == 'threading.Thread'
    assert f'{type(log_cleanup_manager_0.logger).__module__}.{type(log_cleanup_manager_0.logger).__qualname__}' == 'logging.Logger'
    log_cleanup_manager_0.get_cleanup_stats()
    log_cleanup_manager_0.start_cleanup_scheduler()
    log_cleanup_manager_0.stop_cleanup_scheduler()
    log_cleanup_manager_0.cleanup_old_logs()

def test_case_2():
    str_0 = "zF8d$2'J&gI(k"
    log_cleanup_manager_0 = module_0.LogCleanupManager(str_0)
    assert f'{type(log_cleanup_manager_0).__module__}.{type(log_cleanup_manager_0).__qualname__}' == 'snippet_188.LogCleanupManager'
    assert f'{type(log_cleanup_manager_0.log_dir).__module__}.{type(log_cleanup_manager_0.log_dir).__qualname__}' == 'pathlib.PosixPath'
    assert log_cleanup_manager_0.max_age_days == 30
    assert log_cleanup_manager_0.cleanup_interval_hours == 24
    assert log_cleanup_manager_0.cleanup_thread is None
    assert f'{type(log_cleanup_manager_0.stop_event).__module__}.{type(log_cleanup_manager_0.stop_event).__qualname__}' == 'threading.Event'
    assert log_cleanup_manager_0.logger is None
    log_cleanup_manager_0.stop_cleanup_scheduler()

def test_case_3():
    str_0 = ''
    log_cleanup_manager_0 = module_0.LogCleanupManager(str_0)
    assert f'{type(log_cleanup_manager_0).__module__}.{type(log_cleanup_manager_0).__qualname__}' == 'snippet_188.LogCleanupManager'
    assert f'{type(log_cleanup_manager_0.log_dir).__module__}.{type(log_cleanup_manager_0.log_dir).__qualname__}' == 'pathlib.PosixPath'
    assert log_cleanup_manager_0.max_age_days == 30
    assert log_cleanup_manager_0.cleanup_interval_hours == 24
    assert log_cleanup_manager_0.cleanup_thread is None
    assert f'{type(log_cleanup_manager_0.stop_event).__module__}.{type(log_cleanup_manager_0.stop_event).__qualname__}' == 'threading.Event'
    assert log_cleanup_manager_0.logger is None
    log_cleanup_manager_0.cleanup_old_logs()
    log_cleanup_manager_0.stop_cleanup_scheduler()

def test_case_4():
    str_0 = '723M6t~tdw?\x0bdN,zhZ_\r'
    log_cleanup_manager_0 = module_0.LogCleanupManager(str_0, str_0, str_0)
    assert f'{type(log_cleanup_manager_0).__module__}.{type(log_cleanup_manager_0).__qualname__}' == 'snippet_188.LogCleanupManager'
    assert f'{type(log_cleanup_manager_0.log_dir).__module__}.{type(log_cleanup_manager_0.log_dir).__qualname__}' == 'pathlib.PosixPath'
    assert log_cleanup_manager_0.max_age_days == '723M6t~tdw?\x0bdN,zhZ_\r'
    assert log_cleanup_manager_0.cleanup_interval_hours == '723M6t~tdw?\x0bdN,zhZ_\r'
    assert log_cleanup_manager_0.cleanup_thread is None
    assert f'{type(log_cleanup_manager_0.stop_event).__module__}.{type(log_cleanup_manager_0.stop_event).__qualname__}' == 'threading.Event'
    assert log_cleanup_manager_0.logger is None
    log_cleanup_manager_0.cleanup_old_logs()

def test_case_5():
    str_0 = '7(;8'
    log_cleanup_manager_0 = module_0.LogCleanupManager(str_0)
    assert f'{type(log_cleanup_manager_0).__module__}.{type(log_cleanup_manager_0).__qualname__}' == 'snippet_188.LogCleanupManager'
    assert f'{type(log_cleanup_manager_0.log_dir).__module__}.{type(log_cleanup_manager_0.log_dir).__qualname__}' == 'pathlib.PosixPath'
    assert log_cleanup_manager_0.max_age_days == 30
    assert log_cleanup_manager_0.cleanup_interval_hours == 24
    assert log_cleanup_manager_0.cleanup_thread is None
    assert f'{type(log_cleanup_manager_0.stop_event).__module__}.{type(log_cleanup_manager_0.stop_event).__qualname__}' == 'threading.Event'
    assert log_cleanup_manager_0.logger is None
    log_cleanup_manager_0.get_cleanup_stats()
    var_0 = log_cleanup_manager_0.start_cleanup_scheduler()
    assert f'{type(log_cleanup_manager_0.cleanup_thread).__module__}.{type(log_cleanup_manager_0.cleanup_thread).__qualname__}' == 'threading.Thread'
    assert f'{type(log_cleanup_manager_0.logger).__module__}.{type(log_cleanup_manager_0.logger).__qualname__}' == 'logging.Logger'

def test_case_6():
    str_0 = "zF8d$2'J&gI(k"
    log_cleanup_manager_0 = module_0.LogCleanupManager(str_0)
    assert f'{type(log_cleanup_manager_0).__module__}.{type(log_cleanup_manager_0).__qualname__}' == 'snippet_188.LogCleanupManager'
    assert f'{type(log_cleanup_manager_0.log_dir).__module__}.{type(log_cleanup_manager_0.log_dir).__qualname__}' == 'pathlib.PosixPath'
    assert log_cleanup_manager_0.max_age_days == 30
    assert log_cleanup_manager_0.cleanup_interval_hours == 24
    assert log_cleanup_manager_0.cleanup_thread is None
    assert f'{type(log_cleanup_manager_0.stop_event).__module__}.{type(log_cleanup_manager_0.stop_event).__qualname__}' == 'threading.Event'
    assert log_cleanup_manager_0.logger is None

def test_case_7():
    str_0 = 'Hb"_\\E!9UOBX'
    log_cleanup_manager_0 = module_0.LogCleanupManager(str_0)
    assert f'{type(log_cleanup_manager_0).__module__}.{type(log_cleanup_manager_0).__qualname__}' == 'snippet_188.LogCleanupManager'
    assert f'{type(log_cleanup_manager_0.log_dir).__module__}.{type(log_cleanup_manager_0.log_dir).__qualname__}' == 'pathlib.PosixPath'
    assert log_cleanup_manager_0.max_age_days == 30
    assert log_cleanup_manager_0.cleanup_interval_hours == 24
    assert log_cleanup_manager_0.cleanup_thread is None
    assert f'{type(log_cleanup_manager_0.stop_event).__module__}.{type(log_cleanup_manager_0.stop_event).__qualname__}' == 'threading.Event'
    assert log_cleanup_manager_0.logger is None
    var_0 = log_cleanup_manager_0.start_cleanup_scheduler()
    assert f'{type(log_cleanup_manager_0.cleanup_thread).__module__}.{type(log_cleanup_manager_0.cleanup_thread).__qualname__}' == 'threading.Thread'
    assert f'{type(log_cleanup_manager_0.logger).__module__}.{type(log_cleanup_manager_0.logger).__qualname__}' == 'logging.Logger'
    log_cleanup_manager_0.start_cleanup_scheduler()
    log_cleanup_manager_0.stop_cleanup_scheduler()

def test_case_8():
    str_0 = ''
    log_cleanup_manager_0 = module_0.LogCleanupManager(str_0)
    assert f'{type(log_cleanup_manager_0).__module__}.{type(log_cleanup_manager_0).__qualname__}' == 'snippet_188.LogCleanupManager'
    assert f'{type(log_cleanup_manager_0.log_dir).__module__}.{type(log_cleanup_manager_0.log_dir).__qualname__}' == 'pathlib.PosixPath'
    assert log_cleanup_manager_0.max_age_days == 30
    assert log_cleanup_manager_0.cleanup_interval_hours == 24
    assert log_cleanup_manager_0.cleanup_thread is None
    assert f'{type(log_cleanup_manager_0.stop_event).__module__}.{type(log_cleanup_manager_0.stop_event).__qualname__}' == 'threading.Event'
    assert log_cleanup_manager_0.logger is None
    log_cleanup_manager_0.get_cleanup_stats()
    var_0 = log_cleanup_manager_0.start_cleanup_scheduler()
    assert f'{type(log_cleanup_manager_0.cleanup_thread).__module__}.{type(log_cleanup_manager_0.cleanup_thread).__qualname__}' == 'threading.Thread'
    assert f'{type(log_cleanup_manager_0.logger).__module__}.{type(log_cleanup_manager_0.logger).__qualname__}' == 'logging.Logger'
    log_cleanup_manager_0.stop_cleanup_scheduler()
    log_cleanup_manager_0.cleanup_old_logs()