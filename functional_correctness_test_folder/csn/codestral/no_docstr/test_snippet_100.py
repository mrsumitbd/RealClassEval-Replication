import pytest
import snippet_100 as module_0
import cryptography.hazmat.bindings._rust.openssl.ed25519 as module_1

def test_case_0():
    none_type_0 = None
    module_0.Client(none_type_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    module_1.Ed25519PublicKey()