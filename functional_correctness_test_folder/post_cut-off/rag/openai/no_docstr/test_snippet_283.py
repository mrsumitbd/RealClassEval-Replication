import pytest
import snippet_283 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    str_0 = ':'
    module_0.CreateFeedModel(str_0, str_0)

def test_case_1():
    none_type_0 = None
    create_feed_model_0 = module_0.CreateFeedModel(none_type_0, none_type_0)
    assert f'{type(create_feed_model_0).__module__}.{type(create_feed_model_0).__qualname__}' == 'snippet_283.CreateFeedModel'
    assert create_feed_model_0.display_name is None
    assert create_feed_model_0.details is None

def test_case_2():
    none_type_0 = None
    create_feed_model_0 = module_0.CreateFeedModel(none_type_0, none_type_0)
    assert f'{type(create_feed_model_0).__module__}.{type(create_feed_model_0).__qualname__}' == 'snippet_283.CreateFeedModel'
    assert create_feed_model_0.display_name is None
    assert create_feed_model_0.details is None
    create_feed_model_0.to_dict()