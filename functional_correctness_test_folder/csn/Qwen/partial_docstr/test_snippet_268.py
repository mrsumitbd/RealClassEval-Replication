import pytest
import snippet_268 as module_0
import pymonzo.exceptions as module_1

def test_case_0():
    str_0 = '4\rc8#Kb|\\%7d:mst_K68'
    monzo_a_p_i_0 = module_0.MonzoAPI(str_0)
    assert f'{type(monzo_a_p_i_0).__module__}.{type(monzo_a_p_i_0).__qualname__}' == 'snippet_268.MonzoAPI'
    assert f'{type(monzo_a_p_i_0.session).__module__}.{type(monzo_a_p_i_0.session).__qualname__}' == 'authlib.integrations.httpx_client.oauth2_client.OAuth2Client'
    assert f'{type(monzo_a_p_i_0.accounts).__module__}.{type(monzo_a_p_i_0.accounts).__qualname__}' == 'pymonzo.accounts.resources.AccountsResource'
    assert f'{type(monzo_a_p_i_0.attachments).__module__}.{type(monzo_a_p_i_0.attachments).__qualname__}' == 'pymonzo.attachments.resources.AttachmentsResource'
    assert f'{type(monzo_a_p_i_0.balance).__module__}.{type(monzo_a_p_i_0.balance).__qualname__}' == 'pymonzo.balance.resources.BalanceResource'
    assert f'{type(monzo_a_p_i_0.feed).__module__}.{type(monzo_a_p_i_0.feed).__qualname__}' == 'pymonzo.feed.resources.FeedResource'
    assert f'{type(monzo_a_p_i_0.pots).__module__}.{type(monzo_a_p_i_0.pots).__qualname__}' == 'pymonzo.pots.resources.PotsResource'
    assert f'{type(monzo_a_p_i_0.transactions).__module__}.{type(monzo_a_p_i_0.transactions).__qualname__}' == 'pymonzo.transactions.resources.TransactionsResource'
    assert f'{type(monzo_a_p_i_0.webhooks).__module__}.{type(monzo_a_p_i_0.webhooks).__qualname__}' == 'pymonzo.webhooks.resources.WebhooksResource'
    assert module_0.MonzoAPI.api_url == 'https://api.monzo.com'
    assert module_0.MonzoAPI.authorization_endpoint == 'https://auth.monzo.com/'
    assert module_0.MonzoAPI.token_endpoint == 'https://api.monzo.com/oauth2/token'
    assert f'{type(module_0.MonzoAPI.settings_path).__module__}.{type(module_0.MonzoAPI.settings_path).__qualname__}' == 'pathlib.PosixPath'
    assert f'{type(module_0.MonzoAPI.authorize).__module__}.{type(module_0.MonzoAPI.authorize).__qualname__}' == 'builtins.method'

def test_case_1():
    with pytest.raises(module_1.NoSettingsFile):
        module_0.MonzoAPI()