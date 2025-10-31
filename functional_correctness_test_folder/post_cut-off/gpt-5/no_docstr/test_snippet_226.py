import snippet_226 as module_0

def test_case_0():
    price_formatter_0 = module_0.PriceFormatter()
    assert f'{type(price_formatter_0).__module__}.{type(price_formatter_0).__qualname__}' == 'snippet_226.PriceFormatter'
    bool_0 = True
    price_formatter_1 = module_0.PriceFormatter()
    assert f'{type(price_formatter_1).__module__}.{type(price_formatter_1).__qualname__}' == 'snippet_226.PriceFormatter'
    price_formatter_2 = module_0.PriceFormatter()
    assert f'{type(price_formatter_2).__module__}.{type(price_formatter_2).__qualname__}' == 'snippet_226.PriceFormatter'
    str_0 = price_formatter_2.format_price(bool_0, bool_0)
    assert str_0 == '0.0'
    none_type_0 = None
    str_1 = price_formatter_0.format_price_for_display(none_type_0)
    assert str_1 == '$0.0'
    str_2 = price_formatter_1.format_price_for_display(bool_0)
    assert str_2 == '$1.0'
    int_0 = -334
    str_3 = price_formatter_2.format_quantity(int_0)
    assert str_3 == '-334'

def test_case_1():
    int_0 = -1939
    price_formatter_0 = module_0.PriceFormatter()
    assert f'{type(price_formatter_0).__module__}.{type(price_formatter_0).__qualname__}' == 'snippet_226.PriceFormatter'
    str_0 = price_formatter_0.format_price_for_display(int_0)
    assert str_0 == '$-1939.0'

def test_case_2():
    price_formatter_0 = module_0.PriceFormatter()
    assert f'{type(price_formatter_0).__module__}.{type(price_formatter_0).__qualname__}' == 'snippet_226.PriceFormatter'
    none_type_0 = None
    str_0 = price_formatter_0.format_price_for_logging(none_type_0)
    assert str_0 == '$0.0'
    int_0 = 2660
    str_1 = price_formatter_0.format_percentage(int_0)
    assert str_1 == '266000.00%'
    str_2 = price_formatter_0.format_quantity(none_type_0)
    assert str_2 == 'N/A'
    bool_0 = True
    str_3 = price_formatter_0.format_price_for_display(bool_0)
    assert str_3 == '$1.0'
    str_4 = price_formatter_0.format_price_for_logging(str_2)
    assert str_4 == '$0.0'

def test_case_3():
    bytes_0 = b'\xdc\xb1'
    price_formatter_0 = module_0.PriceFormatter()
    assert f'{type(price_formatter_0).__module__}.{type(price_formatter_0).__qualname__}' == 'snippet_226.PriceFormatter'
    str_0 = price_formatter_0.format_price_for_logging(bytes_0)
    assert str_0 == '$0.0'

def test_case_4():
    float_0 = -2354.04
    price_formatter_0 = module_0.PriceFormatter()
    assert f'{type(price_formatter_0).__module__}.{type(price_formatter_0).__qualname__}' == 'snippet_226.PriceFormatter'
    str_0 = price_formatter_0.format_quantity(float_0)
    assert str_0 == '-2354.04'

def test_case_5():
    int_0 = 1327
    price_formatter_0 = module_0.PriceFormatter()
    assert f'{type(price_formatter_0).__module__}.{type(price_formatter_0).__qualname__}' == 'snippet_226.PriceFormatter'
    str_0 = price_formatter_0.format_price_for_logging(int_0)
    assert str_0 == '$1327.0'
    none_type_0 = None
    str_1 = ''
    str_2 = price_formatter_0.format_currency(int_0, str_1)
    assert str_2 == '1327.0 '
    int_1 = -197
    str_3 = price_formatter_0.format_price_for_display(int_1)
    assert str_3 == '$-197.0'
    str_4 = price_formatter_0.format_price_for_logging(none_type_0)
    assert str_4 == '$0.0'
    list_0 = []
    str_5 = price_formatter_0.format_percentage(none_type_0)
    assert str_5 == 'N/A'
    str_6 = price_formatter_0.format_price(list_0, none_type_0)
    assert str_6 == '0.0'

def test_case_6():
    bytes_0 = b'\xdc\xb1'
    price_formatter_0 = module_0.PriceFormatter()
    assert f'{type(price_formatter_0).__module__}.{type(price_formatter_0).__qualname__}' == 'snippet_226.PriceFormatter'
    str_0 = price_formatter_0.format_percentage(bytes_0)
    assert str_0 == 'N/A'
    str_1 = price_formatter_0.format_price_for_logging(bytes_0)
    assert str_1 == '$0.0'

def test_case_7():
    int_0 = -2025
    list_0 = []
    price_formatter_0 = module_0.PriceFormatter(*list_0)
    assert f'{type(price_formatter_0).__module__}.{type(price_formatter_0).__qualname__}' == 'snippet_226.PriceFormatter'
    str_0 = price_formatter_0.format_quantity(price_formatter_0)
    assert str_0 == 'N/A'
    str_1 = price_formatter_0.format_currency(int_0)
    assert str_1 == '$-2025.0'
    int_1 = -2653
    price_formatter_1 = module_0.PriceFormatter()
    assert f'{type(price_formatter_1).__module__}.{type(price_formatter_1).__qualname__}' == 'snippet_226.PriceFormatter'
    str_2 = price_formatter_1.format_price_for_logging(int_1)
    assert str_2 == '$-2653.0'
    price_formatter_2 = module_0.PriceFormatter()
    assert f'{type(price_formatter_2).__module__}.{type(price_formatter_2).__qualname__}' == 'snippet_226.PriceFormatter'
    str_3 = price_formatter_2.format_quantity(int_1)
    assert str_3 == '-2653'
    none_type_0 = None
    str_4 = price_formatter_1.format_price(none_type_0)
    assert str_4 == '0.0'

def test_case_8():
    str_0 = '*LW'
    price_formatter_0 = module_0.PriceFormatter()
    assert f'{type(price_formatter_0).__module__}.{type(price_formatter_0).__qualname__}' == 'snippet_226.PriceFormatter'
    str_1 = price_formatter_0.format_price(str_0)
    assert str_1 == '0.0'

def test_case_9():
    none_type_0 = None
    str_0 = '[Y!CrxTp%/#*'
    price_formatter_0 = module_0.PriceFormatter()
    assert f'{type(price_formatter_0).__module__}.{type(price_formatter_0).__qualname__}' == 'snippet_226.PriceFormatter'
    str_1 = price_formatter_0.format_currency(none_type_0, str_0)
    assert str_1 == '0.0 [Y!CrxTp%/#*'
    set_0 = set()
    price_formatter_1 = module_0.PriceFormatter()
    assert f'{type(price_formatter_1).__module__}.{type(price_formatter_1).__qualname__}' == 'snippet_226.PriceFormatter'
    str_2 = price_formatter_1.format_price(none_type_0)
    assert str_2 == '0.0'
    list_0 = [set_0, set_0]
    str_3 = price_formatter_0.format_price_for_logging(list_0)
    assert str_3 == '$0.0'

def test_case_10():
    int_0 = -2136
    price_formatter_0 = module_0.PriceFormatter()
    assert f'{type(price_formatter_0).__module__}.{type(price_formatter_0).__qualname__}' == 'snippet_226.PriceFormatter'
    str_0 = price_formatter_0.format_percentage(int_0)
    assert str_0 == '-213600.00%'
    str_1 = price_formatter_0.format_currency(int_0)
    assert str_1 == '$-2136.0'

def test_case_11():
    bytes_0 = b',\xae\xea\x0f\\\x82e'
    price_formatter_0 = module_0.PriceFormatter()
    assert f'{type(price_formatter_0).__module__}.{type(price_formatter_0).__qualname__}' == 'snippet_226.PriceFormatter'
    str_0 = price_formatter_0.format_price_for_display(bytes_0)
    assert str_0 == '$0.0'

def test_case_12():
    float_0 = -2354.04
    price_formatter_0 = module_0.PriceFormatter()
    assert f'{type(price_formatter_0).__module__}.{type(price_formatter_0).__qualname__}' == 'snippet_226.PriceFormatter'
    str_0 = price_formatter_0.format_price_for_logging(float_0)
    assert str_0 == '$-2354.039999999999964'
    str_1 = price_formatter_0.format_quantity(float_0)
    assert str_1 == '-2354.04'

def test_case_13():
    float_0 = 1566.7264
    price_formatter_0 = module_0.PriceFormatter()
    assert f'{type(price_formatter_0).__module__}.{type(price_formatter_0).__qualname__}' == 'snippet_226.PriceFormatter'
    str_0 = price_formatter_0.format_currency(float_0)
    assert str_0 == '$1566.7264'
    bool_0 = False
    price_formatter_1 = module_0.PriceFormatter()
    assert f'{type(price_formatter_1).__module__}.{type(price_formatter_1).__qualname__}' == 'snippet_226.PriceFormatter'
    str_1 = price_formatter_1.format_quantity(bool_0)
    assert str_1 == '0'
    str_2 = price_formatter_1.format_price_for_logging(bool_0)
    assert str_2 == '$0.0'

def test_case_14():
    bytes_0 = b'%\xe57R\xaf"6\xf1\xc3\x8a\xbdRt\x80];t\xba\x97'
    tuple_0 = (bytes_0,)
    dict_0 = {}
    price_formatter_0 = module_0.PriceFormatter(**dict_0)
    assert f'{type(price_formatter_0).__module__}.{type(price_formatter_0).__qualname__}' == 'snippet_226.PriceFormatter'
    str_0 = price_formatter_0.format_quantity(tuple_0)
    assert str_0 == 'N/A'

def test_case_15():
    bool_0 = False
    none_type_0 = None
    price_formatter_0 = module_0.PriceFormatter()
    assert f'{type(price_formatter_0).__module__}.{type(price_formatter_0).__qualname__}' == 'snippet_226.PriceFormatter'
    str_0 = price_formatter_0.format_price(bool_0, none_type_0)
    assert str_0 == '0.0'

def test_case_16():
    float_0 = 1566.7264
    price_formatter_0 = module_0.PriceFormatter()
    assert f'{type(price_formatter_0).__module__}.{type(price_formatter_0).__qualname__}' == 'snippet_226.PriceFormatter'
    str_0 = price_formatter_0.format_currency(float_0)
    assert str_0 == '$1566.7264'
    price_formatter_1 = module_0.PriceFormatter()
    assert f'{type(price_formatter_1).__module__}.{type(price_formatter_1).__qualname__}' == 'snippet_226.PriceFormatter'
    str_1 = price_formatter_0.format_price(price_formatter_0)
    assert str_1 == '0.0'
    str_2 = price_formatter_1.format_currency(price_formatter_0)
    assert str_2 == '0.0 USD'

def test_case_17():
    int_0 = 1327
    price_formatter_0 = module_0.PriceFormatter()
    assert f'{type(price_formatter_0).__module__}.{type(price_formatter_0).__qualname__}' == 'snippet_226.PriceFormatter'
    str_0 = price_formatter_0.format_price_for_logging(int_0)
    assert str_0 == '$1327.0'
    none_type_0 = None
    str_1 = ''
    str_2 = price_formatter_0.format_currency(int_0, str_1)
    assert str_2 == '1327.0 '
    int_1 = -197
    str_3 = price_formatter_0.format_price_for_display(int_1)
    assert str_3 == '$-197.0'
    str_4 = price_formatter_0.format_price_for_logging(none_type_0)
    assert str_4 == '$0.0'
    list_0 = []
    str_5 = price_formatter_0.format_price(list_0, none_type_0)
    assert str_5 == '0.0'

def test_case_18():
    float_0 = 1566.7264
    price_formatter_0 = module_0.PriceFormatter()
    assert f'{type(price_formatter_0).__module__}.{type(price_formatter_0).__qualname__}' == 'snippet_226.PriceFormatter'
    str_0 = price_formatter_0.format_currency(float_0)
    assert str_0 == '$1566.7264'
    bool_0 = True
    price_formatter_1 = module_0.PriceFormatter()
    assert f'{type(price_formatter_1).__module__}.{type(price_formatter_1).__qualname__}' == 'snippet_226.PriceFormatter'
    str_1 = price_formatter_1.format_quantity(bool_0)
    assert str_1 == '1'
    str_2 = price_formatter_1.format_price_for_logging(bool_0)
    assert str_2 == '$1.0'

def test_case_19():
    int_0 = 824
    price_formatter_0 = module_0.PriceFormatter()
    assert f'{type(price_formatter_0).__module__}.{type(price_formatter_0).__qualname__}' == 'snippet_226.PriceFormatter'
    str_0 = price_formatter_0.format_currency(int_0, int_0)
    assert str_0 == '824.0 824'
    bool_0 = False
    str_1 = price_formatter_0.format_percentage(bool_0)
    assert str_1 == '0.00%'
    price_formatter_1 = module_0.PriceFormatter()
    assert f'{type(price_formatter_1).__module__}.{type(price_formatter_1).__qualname__}' == 'snippet_226.PriceFormatter'
    str_2 = price_formatter_1.format_price_for_display(bool_0)
    assert str_2 == '$0.0'
    bool_1 = True
    str_3 = price_formatter_1.format_price_for_logging(bool_1)
    assert str_3 == '$1.0'
    price_formatter_2 = module_0.PriceFormatter()
    assert f'{type(price_formatter_2).__module__}.{type(price_formatter_2).__qualname__}' == 'snippet_226.PriceFormatter'
    str_4 = price_formatter_1.format_price(str_3, price_formatter_2)
    assert str_4 == '0.0'
    none_type_0 = None
    str_5 = price_formatter_2.format_price_for_display(none_type_0)
    assert str_5 == '$0.0'

def test_case_20():
    price_formatter_0 = module_0.PriceFormatter()
    assert f'{type(price_formatter_0).__module__}.{type(price_formatter_0).__qualname__}' == 'snippet_226.PriceFormatter'
    float_0 = -1063.308
    str_0 = price_formatter_0.format_price_for_display(float_0)
    assert str_0 == '$-1063.307999999999993'
    bool_0 = True
    str_1 = price_formatter_0.format_price(price_formatter_0, bool_0)
    assert str_1 == '0.0'

def test_case_21():
    bool_0 = True
    dict_0 = {bool_0: bool_0, bool_0: bool_0}
    price_formatter_0 = module_0.PriceFormatter()
    assert f'{type(price_formatter_0).__module__}.{type(price_formatter_0).__qualname__}' == 'snippet_226.PriceFormatter'
    str_0 = price_formatter_0.format_percentage(dict_0)
    assert str_0 == 'N/A'
    bool_1 = False
    price_formatter_1 = module_0.PriceFormatter()
    assert f'{type(price_formatter_1).__module__}.{type(price_formatter_1).__qualname__}' == 'snippet_226.PriceFormatter'
    str_1 = price_formatter_1.format_price(bool_1, bool_1)
    assert str_1 == '0'

def test_case_22():
    int_0 = 528
    price_formatter_0 = module_0.PriceFormatter()
    assert f'{type(price_formatter_0).__module__}.{type(price_formatter_0).__qualname__}' == 'snippet_226.PriceFormatter'
    str_0 = price_formatter_0.format_price(int_0, int_0)
    assert str_0 == '528.0'