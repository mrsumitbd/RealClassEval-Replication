import pytest
import snippet_301 as module_0

def test_case_0():
    dict_0 = {}
    kafka_admin_port_0 = module_0.KafkaAdminPort(**dict_0)
    assert f'{type(kafka_admin_port_0).__module__}.{type(kafka_admin_port_0).__qualname__}' == 'snippet_301.KafkaAdminPort'
    str_0 = ';n}bpNfg7]@>:n+BD'
    with pytest.raises(NotImplementedError):
        kafka_admin_port_0.create_topic(str_0)

def test_case_1():
    list_0 = []
    kafka_admin_port_0 = module_0.KafkaAdminPort()
    assert f'{type(kafka_admin_port_0).__module__}.{type(kafka_admin_port_0).__qualname__}' == 'snippet_301.KafkaAdminPort'
    with pytest.raises(NotImplementedError):
        kafka_admin_port_0.delete_topic(list_0)

def test_case_2():
    kafka_admin_port_0 = module_0.KafkaAdminPort()
    assert f'{type(kafka_admin_port_0).__module__}.{type(kafka_admin_port_0).__qualname__}' == 'snippet_301.KafkaAdminPort'
    with pytest.raises(NotImplementedError):
        kafka_admin_port_0.list_topics()