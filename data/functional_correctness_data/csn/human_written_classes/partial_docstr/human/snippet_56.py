class QA_DataStruct_Future_tick:
    """
    CTP FORMAT
    {'TradingDay': '20181115',
    'InstrumentID': 'rb1901',
    'ExchangeID': '',
    'ExchangeInstID': '',
    'LastPrice': 3874.0,
    'PreSettlementPrice': 3897.0,
    'PreClosePrice': 3937.0,
    'PreOpenInterest': 2429820.0,
    'OpenPrice': 3941.0,
    'HighestPrice': 3946.0,
    'LowestPrice': 3865.0,
    'Volume': 2286142,
    'Turnover': 89450228460.0,
    'OpenInterest': 2482106.0,
    'ClosePrice': 1.7976931348623157e+308,
    'SettlementPrice': 1.7976931348623157e+308,
    'UpperLimitPrice': 4169.0,
    'LowerLimitPrice': 3624.0,
    'PreDelta': 0.0,
    'CurrDelta': 1.7976931348623157e+308,
    'BidPrice1': 3873.0,
    'BidVolume1': 292,
    'AskPrice1': 3874.0,
    'AskVolume1': 223,
    'BidPrice2': 1.7976931348623157e+308,
    'BidVolume2': 0,
    'AskPrice2': 1.7976931348623157e+308,
    'AskVolume2': 0,
    'BidPrice3': 1.7976931348623157e+308,
    'BidVolume3': 0,
    'AskPrice3': 1.7976931348623157e+308,
    'AskVolume3': 0,
    'BidPrice4': 1.7976931348623157e+308,
    'BidVolume4': 0,
    'AskPrice4': 1.7976931348623157e+308,
    'AskVolume4': 0,
    'BidPrice5': 1.7976931348623157e+308,
    'BidVolume5': 0,
    'AskPrice5': 1.7976931348623157e+308,
    'AskVolume5': 0,
    'AveragePrice': 39127.15328269198,
    'ActionDay': '20181115'
    'UpdateTime': '11:30:01',
    'UpdateMillisec': 0,}

    replace(1.7976931348623157e+308, np.nan)
    """

    def __init__(self, data={}):
        self.data = data

    def trading_day(self):
        pass

    def append(self, new_data):
        pass