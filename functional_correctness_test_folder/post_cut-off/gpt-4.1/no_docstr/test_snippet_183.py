import snippet_183 as module_0

def test_case_0():
    str_0 = '&Fos$6*\r"q'
    inference_config_0 = module_0.InferenceConfig(str_0, max_steps=str_0, wandb_project=str_0, use_cached_results=str_0)
    assert f'{type(inference_config_0).__module__}.{type(inference_config_0).__qualname__}' == 'snippet_183.InferenceConfig'
    assert inference_config_0.server_url == '&Fos$6*\r"q'
    assert inference_config_0.server_timeout == 600
    assert inference_config_0.server_max_workers == 48
    assert inference_config_0.batch_size == 32
    assert inference_config_0.max_steps == '&Fos$6*\r"q'
    assert inference_config_0.split == 'test'
    assert inference_config_0.debug is False
    assert inference_config_0.output_dir == 'inference_outputs'
    assert inference_config_0.use_wandb is True
    assert inference_config_0.wandb_project == '&Fos$6*\r"q'
    assert inference_config_0.wandb_entity is None
    assert inference_config_0.show_progress is True
    assert inference_config_0.val_generations_to_log_to_wandb == 10
    assert inference_config_0.skip_generation is False
    assert inference_config_0.use_cached_results == '&Fos$6*\r"q'
    assert inference_config_0.cached_results_path is None
    assert module_0.InferenceConfig.server_url == 'http://localhost:5000'
    assert module_0.InferenceConfig.server_timeout == 600
    assert module_0.InferenceConfig.server_max_workers == 48
    assert module_0.InferenceConfig.batch_size == 32
    assert module_0.InferenceConfig.max_steps == 10
    assert module_0.InferenceConfig.split == 'test'
    assert module_0.InferenceConfig.debug is False
    assert module_0.InferenceConfig.output_dir == 'inference_outputs'
    assert module_0.InferenceConfig.use_wandb is True
    assert module_0.InferenceConfig.wandb_project == 'vagen-inference'
    assert module_0.InferenceConfig.wandb_entity is None
    assert module_0.InferenceConfig.show_progress is True
    assert module_0.InferenceConfig.val_generations_to_log_to_wandb == 10
    assert module_0.InferenceConfig.skip_generation is False
    assert module_0.InferenceConfig.use_cached_results is False
    assert module_0.InferenceConfig.cached_results_path is None
    assert f'{type(module_0.InferenceConfig.from_dict).__module__}.{type(module_0.InferenceConfig.from_dict).__qualname__}' == 'builtins.method'
    assert f'{type(module_0.InferenceConfig.from_yaml).__module__}.{type(module_0.InferenceConfig.from_yaml).__qualname__}' == 'builtins.method'

def test_case_1():
    str_0 = 'Dpj'
    none_type_0 = None
    int_0 = -1282
    inference_config_0 = module_0.InferenceConfig(server_max_workers=int_0, max_steps=int_0, split=str_0, output_dir=none_type_0, wandb_entity=int_0, val_generations_to_log_to_wandb=str_0, cached_results_path=str_0)
    assert f'{type(inference_config_0).__module__}.{type(inference_config_0).__qualname__}' == 'snippet_183.InferenceConfig'
    assert inference_config_0.server_url == 'http://localhost:5000'
    assert inference_config_0.server_timeout == 600
    assert inference_config_0.server_max_workers == -1282
    assert inference_config_0.batch_size == 32
    assert inference_config_0.max_steps == -1282
    assert inference_config_0.split == 'Dpj'
    assert inference_config_0.debug is False
    assert inference_config_0.output_dir is None
    assert inference_config_0.use_wandb is True
    assert inference_config_0.wandb_project == 'vagen-inference'
    assert inference_config_0.wandb_entity == -1282
    assert inference_config_0.show_progress is True
    assert inference_config_0.val_generations_to_log_to_wandb == 'Dpj'
    assert inference_config_0.skip_generation is False
    assert inference_config_0.use_cached_results is False
    assert inference_config_0.cached_results_path == 'Dpj'
    assert module_0.InferenceConfig.server_url == 'http://localhost:5000'
    assert module_0.InferenceConfig.server_timeout == 600
    assert module_0.InferenceConfig.server_max_workers == 48
    assert module_0.InferenceConfig.batch_size == 32
    assert module_0.InferenceConfig.max_steps == 10
    assert module_0.InferenceConfig.split == 'test'
    assert module_0.InferenceConfig.debug is False
    assert module_0.InferenceConfig.output_dir == 'inference_outputs'
    assert module_0.InferenceConfig.use_wandb is True
    assert module_0.InferenceConfig.wandb_project == 'vagen-inference'
    assert module_0.InferenceConfig.wandb_entity is None
    assert module_0.InferenceConfig.show_progress is True
    assert module_0.InferenceConfig.val_generations_to_log_to_wandb == 10
    assert module_0.InferenceConfig.skip_generation is False
    assert module_0.InferenceConfig.use_cached_results is False
    assert module_0.InferenceConfig.cached_results_path is None
    assert f'{type(module_0.InferenceConfig.from_dict).__module__}.{type(module_0.InferenceConfig.from_dict).__qualname__}' == 'builtins.method'
    assert f'{type(module_0.InferenceConfig.from_yaml).__module__}.{type(module_0.InferenceConfig.from_yaml).__qualname__}' == 'builtins.method'

def test_case_2():
    str_0 = 'Ar(0O~-=R!Ptv;Y4I'
    list_0 = []
    bool_0 = False
    bool_1 = False
    inference_config_0 = module_0.InferenceConfig(split=str_0, debug=list_0, show_progress=str_0, val_generations_to_log_to_wandb=bool_0, skip_generation=bool_1)
    assert f'{type(inference_config_0).__module__}.{type(inference_config_0).__qualname__}' == 'snippet_183.InferenceConfig'
    assert inference_config_0.server_url == 'http://localhost:5000'
    assert inference_config_0.server_timeout == 600
    assert inference_config_0.server_max_workers == 48
    assert inference_config_0.batch_size == 32
    assert inference_config_0.max_steps == 10
    assert inference_config_0.split == 'Ar(0O~-=R!Ptv;Y4I'
    assert inference_config_0.debug == []
    assert inference_config_0.output_dir == 'inference_outputs'
    assert inference_config_0.use_wandb is True
    assert inference_config_0.wandb_project == 'vagen-inference'
    assert inference_config_0.wandb_entity is None
    assert inference_config_0.show_progress == 'Ar(0O~-=R!Ptv;Y4I'
    assert inference_config_0.val_generations_to_log_to_wandb is False
    assert inference_config_0.skip_generation is False
    assert inference_config_0.use_cached_results is False
    assert inference_config_0.cached_results_path is None
    assert module_0.InferenceConfig.server_url == 'http://localhost:5000'
    assert module_0.InferenceConfig.server_timeout == 600
    assert module_0.InferenceConfig.server_max_workers == 48
    assert module_0.InferenceConfig.batch_size == 32
    assert module_0.InferenceConfig.max_steps == 10
    assert module_0.InferenceConfig.split == 'test'
    assert module_0.InferenceConfig.debug is False
    assert module_0.InferenceConfig.output_dir == 'inference_outputs'
    assert module_0.InferenceConfig.use_wandb is True
    assert module_0.InferenceConfig.wandb_project == 'vagen-inference'
    assert module_0.InferenceConfig.wandb_entity is None
    assert module_0.InferenceConfig.show_progress is True
    assert module_0.InferenceConfig.val_generations_to_log_to_wandb == 10
    assert module_0.InferenceConfig.skip_generation is False
    assert module_0.InferenceConfig.use_cached_results is False
    assert module_0.InferenceConfig.cached_results_path is None
    assert f'{type(module_0.InferenceConfig.from_dict).__module__}.{type(module_0.InferenceConfig.from_dict).__qualname__}' == 'builtins.method'
    assert f'{type(module_0.InferenceConfig.from_yaml).__module__}.{type(module_0.InferenceConfig.from_yaml).__qualname__}' == 'builtins.method'