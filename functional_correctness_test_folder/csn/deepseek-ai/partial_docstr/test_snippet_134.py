import pytest
import snippet_134 as module_0
import builtins as module_1

@pytest.mark.xfail(strict=True)
def test_case_0():
    bytes_0 = b'\x80\x03\xe2\xb5\x1a\r'
    module_0.Serial2ModbusClient(bytes_0, bytes_0, bytes_0, bytes_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    exception_0 = module_1.Exception()
    none_type_0 = None
    serial2_modbus_client_0 = module_0.Serial2ModbusClient(exception_0, none_type_0)
    assert f'{type(serial2_modbus_client_0).__module__}.{type(serial2_modbus_client_0).__qualname__}' == 'snippet_134.Serial2ModbusClient'
    assert f'{type(serial2_modbus_client_0.serial_w).__module__}.{type(serial2_modbus_client_0.serial_w).__qualname__}' == 'builtins.Exception'
    assert serial2_modbus_client_0.mbus_cli is None
    assert serial2_modbus_client_0.slave_addr == 1
    assert serial2_modbus_client_0.allow_bcast is False
    assert module_0.EXP_GATEWAY_TARGET_DEVICE_FAILED_TO_RESPOND == 11
    serial2_modbus_client_0.run()