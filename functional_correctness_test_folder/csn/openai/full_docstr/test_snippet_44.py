import pytest
import snippet_44 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    event_webhook_0 = module_0.EventWebhook()
    module_0.EventWebhook(event_webhook_0)

def test_case_1():
    module_0.EventWebhook()

@pytest.mark.xfail(strict=True)
def test_case_2():
    event_webhook_0 = module_0.EventWebhook()
    event_webhook_0.convert_public_key_to_ecdsa(event_webhook_0)