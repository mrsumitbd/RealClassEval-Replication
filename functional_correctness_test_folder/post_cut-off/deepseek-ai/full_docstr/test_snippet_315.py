import pytest
import snippet_315 as module_0
import bedrock_server_manager.error as module_1

@pytest.mark.xfail(strict=True)
def test_case_0():
    player_mixin_0 = module_0.PlayerMixin()
    assert f'{type(player_mixin_0).__module__}.{type(player_mixin_0).__qualname__}' == 'snippet_315.PlayerMixin'
    assert module_0.TYPE_CHECKING is False
    str_0 = ' \t^/"'
    player_mixin_0.parse_player_cli_argument(str_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    player_mixin_0 = module_0.PlayerMixin()
    assert f'{type(player_mixin_0).__module__}.{type(player_mixin_0).__qualname__}' == 'snippet_315.PlayerMixin'
    assert module_0.TYPE_CHECKING is False
    none_type_0 = player_mixin_0.parse_player_cli_argument(player_mixin_0)
    player_mixin_0.parse_player_cli_argument(none_type_0)
    str_0 = "4'h1W-}@WW4t"
    player_mixin_0.parse_player_cli_argument(str_0)

@pytest.mark.xfail(strict=True)
def test_case_2():
    player_mixin_0 = module_0.PlayerMixin()
    assert f'{type(player_mixin_0).__module__}.{type(player_mixin_0).__qualname__}' == 'snippet_315.PlayerMixin'
    assert module_0.TYPE_CHECKING is False
    list_0 = []
    player_mixin_0.save_player_data(list_0)

def test_case_3():
    set_0 = set()
    player_mixin_0 = module_0.PlayerMixin()
    assert f'{type(player_mixin_0).__module__}.{type(player_mixin_0).__qualname__}' == 'snippet_315.PlayerMixin'
    assert module_0.TYPE_CHECKING is False
    with pytest.raises(module_1.UserInputError):
        player_mixin_0.save_player_data(set_0)

def test_case_4():
    player_mixin_0 = module_0.PlayerMixin()
    assert f'{type(player_mixin_0).__module__}.{type(player_mixin_0).__qualname__}' == 'snippet_315.PlayerMixin'
    assert module_0.TYPE_CHECKING is False
    str_0 = ' \t^/"'
    dict_0 = {str_0: str_0}
    list_0 = [dict_0]
    with pytest.raises(module_1.UserInputError):
        player_mixin_0.save_player_data(list_0)

def test_case_5():
    none_type_0 = None
    player_mixin_0 = module_0.PlayerMixin()
    assert f'{type(player_mixin_0).__module__}.{type(player_mixin_0).__qualname__}' == 'snippet_315.PlayerMixin'
    assert module_0.TYPE_CHECKING is False
    none_type_1 = player_mixin_0.parse_player_cli_argument(player_mixin_0)
    player_mixin_0.parse_player_cli_argument(none_type_1)
    list_0 = [none_type_0, none_type_0, none_type_0]
    with pytest.raises(module_1.UserInputError):
        player_mixin_0.save_player_data(list_0)