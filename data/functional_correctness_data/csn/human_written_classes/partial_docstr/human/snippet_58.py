from QUANTAXIS.QAUtil.QASql import QA_util_sql_mongo_setting
from QUANTAXIS.QAFetch import QATdx as QATdx
from QUANTAXIS.QAFetch import QAQuery
from QUANTAXIS.QAUtil.QAParameter import DATABASE_TABLE, DATASOURCE, FREQUENCE, MARKET_TYPE, OUTPUT_FORMAT

class QA_Fetcher:

    def __init__(self, uri='mongodb://127.0.0.1:27017/quantaxis', username='', password=''):
        """
        初始化的时候 会初始化
        """
        self.database = QA_util_sql_mongo_setting(uri).quantaxis
        self.history = {}
        self.best_ip = QATdx.select_best_ip()

    def change_ip(self, uri):
        self.database = QA_util_sql_mongo_setting(uri).quantaxis
        return self

    def get_quotation(self, code=None, start=None, end=None, frequence=None, market=None, source=None, output=None):
        """        
        Arguments:
            code {str/list} -- 证券/股票的代码
            start {str} -- 开始日期
            end {str} -- 结束日期
            frequence {enum} -- 频率 QA.FREQUENCE
            market {enum} -- 市场 QA.MARKET_TYPE
            source {enum} -- 来源 QA.DATASOURCE
            output {enum} -- 输出类型 QA.OUTPUT_FORMAT
        """
        pass

    def get_info(self, code, frequence, market, source, output):
        if source is DATASOURCE.TDX:
            res = QATdx.QA_fetch_get_stock_info(code, self.best_ip)
            return res
        elif source is DATASOURCE.MONGO:
            res = QAQuery.QA_fetch_stock_info(code, format=output, collections=self.database.stock_info)
            return res