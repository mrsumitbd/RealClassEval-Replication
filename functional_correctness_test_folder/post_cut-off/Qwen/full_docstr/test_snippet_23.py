import snippet_23 as module_0

def test_case_0():
    git_hub_u_r_l_extractor_0 = module_0.GitHubURLExtractor()
    assert f'{type(git_hub_u_r_l_extractor_0).__module__}.{type(git_hub_u_r_l_extractor_0).__qualname__}' == 'snippet_23.GitHubURLExtractor'
    str_0 = 'HyU'
    git_hub_u_r_l_extractor_0.extract_github_urls(str_0)

def test_case_1():
    git_hub_u_r_l_extractor_0 = module_0.GitHubURLExtractor()
    assert f'{type(git_hub_u_r_l_extractor_0).__module__}.{type(git_hub_u_r_l_extractor_0).__qualname__}' == 'snippet_23.GitHubURLExtractor'
    str_0 = 'KN{~7>'
    git_hub_u_r_l_extractor_0.extract_target_path(str_0)

def test_case_2():
    git_hub_u_r_l_extractor_0 = module_0.GitHubURLExtractor()
    assert f'{type(git_hub_u_r_l_extractor_0).__module__}.{type(git_hub_u_r_l_extractor_0).__qualname__}' == 'snippet_23.GitHubURLExtractor'
    str_0 = '>5j\\6.3;{:R"'
    str_1 = git_hub_u_r_l_extractor_0.infer_repo_name(str_0)
    assert str_1 == 'repository'

def test_case_3():
    git_hub_u_r_l_extractor_0 = module_0.GitHubURLExtractor()
    assert f'{type(git_hub_u_r_l_extractor_0).__module__}.{type(git_hub_u_r_l_extractor_0).__qualname__}' == 'snippet_23.GitHubURLExtractor'
    str_0 = 'M/Cq'
    git_hub_u_r_l_extractor_0.extract_target_path(str_0)
    git_hub_u_r_l_extractor_0.extract_github_urls(str_0)
    str_1 = '5N +lXPgK+Iw^CP;&O+'
    str_2 = git_hub_u_r_l_extractor_0.infer_repo_name(str_1)
    assert str_2 == 'repository'

def test_case_4():
    git_hub_u_r_l_extractor_0 = module_0.GitHubURLExtractor()
    assert f'{type(git_hub_u_r_l_extractor_0).__module__}.{type(git_hub_u_r_l_extractor_0).__qualname__}' == 'snippet_23.GitHubURLExtractor'
    str_0 = '_/Cq'
    str_1 = '71HoLcHmq,\\O=fhf'
    str_2 = git_hub_u_r_l_extractor_0.infer_repo_name(str_1)
    assert str_2 == 'repository'
    git_hub_u_r_l_extractor_0.extract_github_urls(str_0)
    git_hub_u_r_l_extractor_0.extract_target_path(str_2)