import pytest
import snippet_284 as module_0

def test_case_0():
    update_feed_model_0 = module_0.UpdateFeedModel()
    assert f'{type(update_feed_model_0).__module__}.{type(update_feed_model_0).__qualname__}' == 'snippet_284.UpdateFeedModel'
    assert update_feed_model_0.display_name is None
    assert update_feed_model_0.details is None
    assert module_0.UpdateFeedModel.display_name is None
    assert module_0.UpdateFeedModel.details is None

def test_case_1():
    update_feed_model_0 = module_0.UpdateFeedModel()
    assert f'{type(update_feed_model_0).__module__}.{type(update_feed_model_0).__qualname__}' == 'snippet_284.UpdateFeedModel'
    assert update_feed_model_0.display_name is None
    assert update_feed_model_0.details is None
    assert module_0.UpdateFeedModel.display_name is None
    assert module_0.UpdateFeedModel.details is None
    update_feed_model_0.to_dict()

@pytest.mark.xfail(strict=True)
def test_case_2():
    str_0 = 'Im#-;}U'
    module_0.UpdateFeedModel(details=str_0)