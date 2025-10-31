import pytest
import snippet_358 as module_0

def test_case_0():
    residual_connection_0 = module_0.ResidualConnection()
    none_type_0 = None
    residual_connection_0.register(none_type_0)
    residual_connection_1 = module_0.ResidualConnection()
    residual_connection_0.apply(residual_connection_1)

def test_case_1():
    residual_connection_0 = module_0.ResidualConnection()
    with pytest.raises(RuntimeError):
        residual_connection_0.apply(residual_connection_0)

def test_case_2():
    module_0.ResidualConnection()

def test_case_3():
    residual_connection_0 = module_0.ResidualConnection()
    residual_connection_0.register(residual_connection_0)