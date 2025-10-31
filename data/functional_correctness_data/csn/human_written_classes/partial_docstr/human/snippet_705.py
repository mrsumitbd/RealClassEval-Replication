class FakePandas:
    """Typing in Device requires pandas, but it is not available"""

    class DataFrame:
        id = 'fake'

    def sql(self):
        return None

    def Timestamp(self):
        return None