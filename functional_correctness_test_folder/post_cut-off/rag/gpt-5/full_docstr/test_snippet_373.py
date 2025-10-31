import snippet_373 as module_0

def test_case_0():
    str_0 = "\x0c9X)(D'wBsx}O#|M"
    t_p_c_data_generator_0 = module_0._TPCDataGenerator(str_0)
    assert f'{type(t_p_c_data_generator_0).__module__}.{type(t_p_c_data_generator_0).__qualname__}' == 'snippet_373._TPCDataGenerator'
    assert t_p_c_data_generator_0.scale_factor == "\x0c9X)(D'wBsx}O#|M"
    assert t_p_c_data_generator_0.target_mount_folder_path is None
    assert t_p_c_data_generator_0.target_row_group_size_mb == 128
    assert module_0._TPCDataGenerator.GEN_UTIL == ''