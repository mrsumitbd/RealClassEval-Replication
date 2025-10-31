import pytest
import snippet_239 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    str_0 = '75/S@K<\x0cQ:b)~!+o'
    none_type_0 = None
    module_0.Partner(str_0, verify_cert_ca=none_type_0, compress=str_0, enc_alg=none_type_0, digest_alg=str_0, sign_alg=none_type_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    none_type_0 = None
    partner_0 = module_0.Partner(none_type_0, verify_cert_ca=none_type_0, encrypt_cert_ca=none_type_0, sign=none_type_0, mdn_digest_alg=none_type_0)
    assert f'{type(partner_0).__module__}.{type(partner_0).__qualname__}' == 'snippet_239.Partner'
    assert partner_0.as2_name is None
    assert partner_0.verify_cert is None
    assert partner_0.verify_cert_ca is None
    assert partner_0.encrypt_cert is None
    assert partner_0.encrypt_cert_ca is None
    assert partner_0.validate_certs is True
    assert partner_0.compress is False
    assert partner_0.encrypt is False
    assert partner_0.enc_alg == 'tripledes_192_cbc'
    assert partner_0.sign is None
    assert partner_0.digest_alg == 'sha256'
    assert partner_0.mdn_mode is None
    assert partner_0.mdn_digest_alg is None
    assert partner_0.mdn_confirm_text == 'The AS2 message has been successfully processed. Thank you for exchanging AS2 messages with pyAS2.'
    assert partner_0.ignore_self_signed is True
    assert partner_0.canonicalize_as_binary is False
    assert partner_0.sign_alg == 'rsassa_pkcs1v15'
    assert partner_0.key_enc_alg == 'rsaes_pkcs1v15'
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
    assert module_0.Partner.verify_cert is None
    assert module_0.Partner.verify_cert_ca is None
    assert module_0.Partner.encrypt_cert is None
    assert module_0.Partner.encrypt_cert_ca is None
    assert module_0.Partner.validate_certs is True
    assert module_0.Partner.compress is False
    assert module_0.Partner.encrypt is False
    assert module_0.Partner.enc_alg == 'tripledes_192_cbc'
    assert module_0.Partner.sign is False
    assert module_0.Partner.digest_alg == 'sha256'
    assert module_0.Partner.mdn_mode is None
    assert module_0.Partner.mdn_digest_alg is None
    assert module_0.Partner.mdn_confirm_text == 'The AS2 message has been successfully processed. Thank you for exchanging AS2 messages with pyAS2.'
    assert module_0.Partner.ignore_self_signed is True
    assert module_0.Partner.canonicalize_as_binary is False
    assert module_0.Partner.sign_alg == 'rsassa_pkcs1v15'
    assert module_0.Partner.key_enc_alg == 'rsaes_pkcs1v15'
    str_0 = 'K)pZ}N_WG,d'
    bool_0 = True
    bool_1 = False
    bool_2 = False
    partner_1 = module_0.Partner(bool_0, bool_1, validate_certs=bool_2, encrypt=str_0, enc_alg=bool_2)
    assert f'{type(partner_1).__module__}.{type(partner_1).__qualname__}' == 'snippet_239.Partner'
    assert partner_1.as2_name is True
    assert partner_1.verify_cert is False
    assert partner_1.verify_cert_ca is None
    assert partner_1.encrypt_cert is None
    assert partner_1.encrypt_cert_ca is None
    assert partner_1.validate_certs is False
    assert partner_1.compress is False
    assert partner_1.encrypt == 'K)pZ}N_WG,d'
    assert partner_1.enc_alg is False
    assert partner_1.sign is False
    assert partner_1.digest_alg == 'sha256'
    assert partner_1.mdn_mode is None
    assert partner_1.mdn_digest_alg is None
    assert partner_1.mdn_confirm_text == 'The AS2 message has been successfully processed. Thank you for exchanging AS2 messages with pyAS2.'
    assert partner_1.ignore_self_signed is True
    assert partner_1.canonicalize_as_binary is False
    assert partner_1.sign_alg == 'rsassa_pkcs1v15'
    assert partner_1.key_enc_alg == 'rsaes_pkcs1v15'
    partner_1.load_encrypt_cert()

def test_case_2():
    bytes_0 = b'\\z\x94\xf3,,^\xe4\xf7zhZ\xa8\xa6\x1f'
    bool_0 = False
    partner_0 = module_0.Partner(bytes_0, encrypt_cert_ca=bytes_0, validate_certs=bool_0, mdn_mode=bool_0, key_enc_alg=bool_0)
    assert f'{type(partner_0).__module__}.{type(partner_0).__qualname__}' == 'snippet_239.Partner'
    assert partner_0.as2_name == b'\\z\x94\xf3,,^\xe4\xf7zhZ\xa8\xa6\x1f'
    assert partner_0.verify_cert is None
    assert partner_0.verify_cert_ca is None
    assert partner_0.encrypt_cert is None
    assert partner_0.encrypt_cert_ca == b'\\z\x94\xf3,,^\xe4\xf7zhZ\xa8\xa6\x1f'
    assert partner_0.validate_certs is False
    assert partner_0.compress is False
    assert partner_0.encrypt is False
    assert partner_0.enc_alg == 'tripledes_192_cbc'
    assert partner_0.sign is False
    assert partner_0.digest_alg == 'sha256'
    assert partner_0.mdn_mode is False
    assert partner_0.mdn_digest_alg is None
    assert partner_0.mdn_confirm_text == 'The AS2 message has been successfully processed. Thank you for exchanging AS2 messages with pyAS2.'
    assert partner_0.ignore_self_signed is True
    assert partner_0.canonicalize_as_binary is False
    assert partner_0.sign_alg == 'rsassa_pkcs1v15'
    assert partner_0.key_enc_alg is False
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
    assert module_0.Partner.verify_cert is None
    assert module_0.Partner.verify_cert_ca is None
    assert module_0.Partner.encrypt_cert is None
    assert module_0.Partner.encrypt_cert_ca is None
    assert module_0.Partner.validate_certs is True
    assert module_0.Partner.compress is False
    assert module_0.Partner.encrypt is False
    assert module_0.Partner.enc_alg == 'tripledes_192_cbc'
    assert module_0.Partner.sign is False
    assert module_0.Partner.digest_alg == 'sha256'
    assert module_0.Partner.mdn_mode is None
    assert module_0.Partner.mdn_digest_alg is None
    assert module_0.Partner.mdn_confirm_text == 'The AS2 message has been successfully processed. Thank you for exchanging AS2 messages with pyAS2.'
    assert module_0.Partner.ignore_self_signed is True
    assert module_0.Partner.canonicalize_as_binary is False
    assert module_0.Partner.sign_alg == 'rsassa_pkcs1v15'
    assert module_0.Partner.key_enc_alg == 'rsaes_pkcs1v15'

@pytest.mark.xfail(strict=True)
def test_case_3():
    none_type_0 = None
    none_type_1 = None
    bool_0 = False
    str_0 = "r~HtG]'Q"
    module_0.Partner(str_0, verify_cert_ca=bool_0, encrypt_cert=none_type_0, encrypt=bool_0, enc_alg=str_0, mdn_confirm_text=none_type_1, canonicalize_as_binary=none_type_0)

@pytest.mark.xfail(strict=True)
def test_case_4():
    str_0 = '~'
    bytes_0 = b''
    bool_0 = True
    module_0.Partner(str_0, str_0, encrypt_cert=bytes_0, sign=bool_0, mdn_digest_alg=str_0, mdn_confirm_text=bool_0, ignore_self_signed=bool_0, canonicalize_as_binary=bytes_0, key_enc_alg=str_0)

@pytest.mark.xfail(strict=True)
def test_case_5():
    str_0 = ''
    none_type_0 = None
    bool_0 = False
    bool_1 = False
    partner_0 = module_0.Partner(str_0, encrypt_cert=none_type_0, encrypt_cert_ca=none_type_0, sign=bool_0, ignore_self_signed=bool_1, sign_alg=none_type_0)
    assert f'{type(partner_0).__module__}.{type(partner_0).__qualname__}' == 'snippet_239.Partner'
    assert partner_0.as2_name == ''
    assert partner_0.verify_cert is None
    assert partner_0.verify_cert_ca is None
    assert partner_0.encrypt_cert is None
    assert partner_0.encrypt_cert_ca is None
    assert partner_0.validate_certs is True
    assert partner_0.compress is False
    assert partner_0.encrypt is False
    assert partner_0.enc_alg == 'tripledes_192_cbc'
    assert partner_0.sign is False
    assert partner_0.digest_alg == 'sha256'
    assert partner_0.mdn_mode is None
    assert partner_0.mdn_digest_alg is None
    assert partner_0.mdn_confirm_text == 'The AS2 message has been successfully processed. Thank you for exchanging AS2 messages with pyAS2.'
    assert partner_0.ignore_self_signed is False
    assert partner_0.canonicalize_as_binary is False
    assert partner_0.sign_alg is None
    assert partner_0.key_enc_alg == 'rsaes_pkcs1v15'
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
    assert module_0.Partner.verify_cert is None
    assert module_0.Partner.verify_cert_ca is None
    assert module_0.Partner.encrypt_cert is None
    assert module_0.Partner.encrypt_cert_ca is None
    assert module_0.Partner.validate_certs is True
    assert module_0.Partner.compress is False
    assert module_0.Partner.encrypt is False
    assert module_0.Partner.enc_alg == 'tripledes_192_cbc'
    assert module_0.Partner.sign is False
    assert module_0.Partner.digest_alg == 'sha256'
    assert module_0.Partner.mdn_mode is None
    assert module_0.Partner.mdn_digest_alg is None
    assert module_0.Partner.mdn_confirm_text == 'The AS2 message has been successfully processed. Thank you for exchanging AS2 messages with pyAS2.'
    assert module_0.Partner.ignore_self_signed is True
    assert module_0.Partner.canonicalize_as_binary is False
    assert module_0.Partner.sign_alg == 'rsassa_pkcs1v15'
    assert module_0.Partner.key_enc_alg == 'rsaes_pkcs1v15'
    partner_0.load_verify_cert()

@pytest.mark.xfail(strict=True)
def test_case_6():
    bool_0 = True
    str_0 = '^ W@-N[+6Yp!bv5ND'
    bool_1 = True
    str_1 = '.#\ntC>u1'
    module_0.Partner(str_0, encrypt_cert=bool_0, encrypt=bool_1, mdn_confirm_text=str_1, ignore_self_signed=bool_1, key_enc_alg=str_0)

@pytest.mark.xfail(strict=True)
def test_case_7():
    none_type_0 = None
    str_0 = ''
    partner_0 = module_0.Partner(str_0, validate_certs=str_0, digest_alg=str_0, ignore_self_signed=none_type_0)
    assert f'{type(partner_0).__module__}.{type(partner_0).__qualname__}' == 'snippet_239.Partner'
    assert partner_0.as2_name == ''
    assert partner_0.verify_cert is None
    assert partner_0.verify_cert_ca is None
    assert partner_0.encrypt_cert is None
    assert partner_0.encrypt_cert_ca is None
    assert partner_0.validate_certs == ''
    assert partner_0.compress is False
    assert partner_0.encrypt is False
    assert partner_0.enc_alg == 'tripledes_192_cbc'
    assert partner_0.sign is False
    assert partner_0.digest_alg == ''
    assert partner_0.mdn_mode is None
    assert partner_0.mdn_digest_alg is None
    assert partner_0.mdn_confirm_text == 'The AS2 message has been successfully processed. Thank you for exchanging AS2 messages with pyAS2.'
    assert partner_0.ignore_self_signed is None
    assert partner_0.canonicalize_as_binary is False
    assert partner_0.sign_alg == 'rsassa_pkcs1v15'
    assert partner_0.key_enc_alg == 'rsaes_pkcs1v15'
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
    assert module_0.Partner.verify_cert is None
    assert module_0.Partner.verify_cert_ca is None
    assert module_0.Partner.encrypt_cert is None
    assert module_0.Partner.encrypt_cert_ca is None
    assert module_0.Partner.validate_certs is True
    assert module_0.Partner.compress is False
    assert module_0.Partner.encrypt is False
    assert module_0.Partner.enc_alg == 'tripledes_192_cbc'
    assert module_0.Partner.sign is False
    assert module_0.Partner.digest_alg == 'sha256'
    assert module_0.Partner.mdn_mode is None
    assert module_0.Partner.mdn_digest_alg is None
    assert module_0.Partner.mdn_confirm_text == 'The AS2 message has been successfully processed. Thank you for exchanging AS2 messages with pyAS2.'
    assert module_0.Partner.ignore_self_signed is True
    assert module_0.Partner.canonicalize_as_binary is False
    assert module_0.Partner.sign_alg == 'rsassa_pkcs1v15'
    assert module_0.Partner.key_enc_alg == 'rsaes_pkcs1v15'
    partner_0.load_verify_cert()

@pytest.mark.xfail(strict=True)
def test_case_8():
    str_0 = 'f^}'
    none_type_0 = None
    bool_0 = True
    module_0.Partner(str_0, verify_cert_ca=none_type_0, encrypt_cert_ca=none_type_0, compress=bool_0, mdn_mode=str_0, mdn_confirm_text=str_0, canonicalize_as_binary=none_type_0, sign_alg=none_type_0, key_enc_alg=none_type_0)

@pytest.mark.xfail(strict=True)
def test_case_9():
    none_type_0 = None
    str_0 = 'K)pZ}N_W_G,d'
    bool_0 = True
    bool_1 = True
    partner_0 = module_0.Partner(str_0, validate_certs=bool_0, compress=bool_1, encrypt=bool_1, sign=str_0, mdn_mode=none_type_0)
    assert f'{type(partner_0).__module__}.{type(partner_0).__qualname__}' == 'snippet_239.Partner'
    assert partner_0.as2_name == 'K)pZ}N_W_G,d'
    assert partner_0.verify_cert is None
    assert partner_0.verify_cert_ca is None
    assert partner_0.encrypt_cert is None
    assert partner_0.encrypt_cert_ca is None
    assert partner_0.validate_certs is True
    assert partner_0.compress is True
    assert partner_0.encrypt is True
    assert partner_0.enc_alg == 'tripledes_192_cbc'
    assert partner_0.sign == 'K)pZ}N_W_G,d'
    assert partner_0.digest_alg == 'sha256'
    assert partner_0.mdn_mode is None
    assert partner_0.mdn_digest_alg is None
    assert partner_0.mdn_confirm_text == 'The AS2 message has been successfully processed. Thank you for exchanging AS2 messages with pyAS2.'
    assert partner_0.ignore_self_signed is True
    assert partner_0.canonicalize_as_binary is False
    assert partner_0.sign_alg == 'rsassa_pkcs1v15'
    assert partner_0.key_enc_alg == 'rsaes_pkcs1v15'
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
    assert module_0.Partner.verify_cert is None
    assert module_0.Partner.verify_cert_ca is None
    assert module_0.Partner.encrypt_cert is None
    assert module_0.Partner.encrypt_cert_ca is None
    assert module_0.Partner.validate_certs is True
    assert module_0.Partner.compress is False
    assert module_0.Partner.encrypt is False
    assert module_0.Partner.enc_alg == 'tripledes_192_cbc'
    assert module_0.Partner.sign is False
    assert module_0.Partner.digest_alg == 'sha256'
    assert module_0.Partner.mdn_mode is None
    assert module_0.Partner.mdn_digest_alg is None
    assert module_0.Partner.mdn_confirm_text == 'The AS2 message has been successfully processed. Thank you for exchanging AS2 messages with pyAS2.'
    assert module_0.Partner.ignore_self_signed is True
    assert module_0.Partner.canonicalize_as_binary is False
    assert module_0.Partner.sign_alg == 'rsassa_pkcs1v15'
    assert module_0.Partner.key_enc_alg == 'rsaes_pkcs1v15'
    partner_0.load_encrypt_cert()

@pytest.mark.xfail(strict=True)
def test_case_10():
    none_type_0 = None
    int_0 = 928
    partner_0 = module_0.Partner(int_0, encrypt_cert=none_type_0, validate_certs=none_type_0, enc_alg=none_type_0, canonicalize_as_binary=int_0)
    assert f'{type(partner_0).__module__}.{type(partner_0).__qualname__}' == 'snippet_239.Partner'
    assert partner_0.as2_name == 928
    assert partner_0.verify_cert is None
    assert partner_0.verify_cert_ca is None
    assert partner_0.encrypt_cert is None
    assert partner_0.encrypt_cert_ca is None
    assert partner_0.validate_certs is None
    assert partner_0.compress is False
    assert partner_0.encrypt is False
    assert partner_0.enc_alg is None
    assert partner_0.sign is False
    assert partner_0.digest_alg == 'sha256'
    assert partner_0.mdn_mode is None
    assert partner_0.mdn_digest_alg is None
    assert partner_0.mdn_confirm_text == 'The AS2 message has been successfully processed. Thank you for exchanging AS2 messages with pyAS2.'
    assert partner_0.ignore_self_signed is True
    assert partner_0.canonicalize_as_binary == 928
    assert partner_0.sign_alg == 'rsassa_pkcs1v15'
    assert partner_0.key_enc_alg == 'rsaes_pkcs1v15'
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
    assert module_0.Partner.verify_cert is None
    assert module_0.Partner.verify_cert_ca is None
    assert module_0.Partner.encrypt_cert is None
    assert module_0.Partner.encrypt_cert_ca is None
    assert module_0.Partner.validate_certs is True
    assert module_0.Partner.compress is False
    assert module_0.Partner.encrypt is False
    assert module_0.Partner.enc_alg == 'tripledes_192_cbc'
    assert module_0.Partner.sign is False
    assert module_0.Partner.digest_alg == 'sha256'
    assert module_0.Partner.mdn_mode is None
    assert module_0.Partner.mdn_digest_alg is None
    assert module_0.Partner.mdn_confirm_text == 'The AS2 message has been successfully processed. Thank you for exchanging AS2 messages with pyAS2.'
    assert module_0.Partner.ignore_self_signed is True
    assert module_0.Partner.canonicalize_as_binary is False
    assert module_0.Partner.sign_alg == 'rsassa_pkcs1v15'
    assert module_0.Partner.key_enc_alg == 'rsaes_pkcs1v15'
    partner_0.load_verify_cert()

@pytest.mark.xfail(strict=True)
def test_case_11():
    none_type_0 = None
    bool_0 = False
    str_0 = 'rX*Y\t*1EZEx]Z;s4)jW*'
    module_0.Partner(str_0, enc_alg=bool_0, mdn_mode=none_type_0, sign_alg=str_0)