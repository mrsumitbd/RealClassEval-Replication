import pytest
import snippet_238 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    str_0 = '{?[oI+#H"[V=.W9'
    bytes_0 = b"\x83\x98\xb2\xa0=4\xf6\xdc\x1d\xa3'\xaf%\xa3"
    module_0.Organization(str_0, bytes_0, str_0, mdn_url=str_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    bytes_0 = b'\x03\xd5\xa8\xa3J'
    str_0 = 'A3'
    module_0.Organization(str_0, decrypt_key=bytes_0, domain=str_0)

def test_case_2():
    none_type_0 = None
    str_0 = 's}P'
    organization_0 = module_0.Organization(str_0, domain=none_type_0)
    assert f'{type(organization_0).__module__}.{type(organization_0).__qualname__}' == 'snippet_238.Organization'
    assert organization_0.as2_name == 's}P'
    assert organization_0.sign_key is None
    assert organization_0.sign_key_pass is None
    assert organization_0.decrypt_key is None
    assert organization_0.decrypt_key_pass is None
    assert organization_0.mdn_url is None
    assert organization_0.mdn_confirm_text == 'The AS2 message has been successfully processed. Thank you for exchanging AS2 messages with pyAS2.'
    assert organization_0.domain is None
    assert module_0.AS2_VERSION == '1.2'
    assert module_0.ASYNCHRONOUS_MDN == 'ASYNC'
    assert module_0.DIGEST_ALGORITHMS == ('md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512')
    assert module_0.EDIINT_FEATURES == 'CMS'
    assert module_0.ENCRYPTION_ALGORITHMS == ('tripledes_192_cbc', 'rc2_128_cbc', 'rc4_128_cbc', 'aes_128_cbc', 'aes_192_cbc', 'aes_256_cbc')
    assert module_0.KEY_ENCRYPTION_ALGORITHMS == ('rsaes_pkcs1v15', 'rsaes_oaep')
    assert module_0.MDN_CONFIRM_TEXT == 'The AS2 message has been successfully processed. Thank you for exchanging AS2 messages with pyAS2.'
    assert module_0.MDN_FAILED_TEXT == 'The AS2 message could not be processed. The disposition-notification report has additional details.'
    assert module_0.MDN_MODES == ('SYNC', 'ASYNC')
    assert module_0.SIGNATUR_ALGORITHMS == ('rsassa_pkcs1v15', 'rsassa_pss')
    assert module_0.SYNCHRONOUS_MDN == 'SYNC'
    assert module_0.Organization.sign_key is None
    assert module_0.Organization.sign_key_pass is None
    assert module_0.Organization.decrypt_key is None
    assert module_0.Organization.decrypt_key_pass is None
    assert module_0.Organization.mdn_url is None
    assert module_0.Organization.mdn_confirm_text == 'The AS2 message has been successfully processed. Thank you for exchanging AS2 messages with pyAS2.'
    assert module_0.Organization.domain is None

@pytest.mark.xfail(strict=True)
def test_case_3():
    str_0 = 'S'
    module_0.Organization(str_0, decrypt_key=str_0, mdn_url=str_0)

def test_case_4():
    none_type_0 = None