from typing import Optional, Text

class MashStep:

    def __init__(self):
        self.name: Optional[Text] = None
        self.type: Optional[Text] = None
        self.infuse_amount: Optional[float] = None
        self.step_temp: Optional[float] = None
        self.end_temp: Optional[float] = None
        self.step_time: Optional[float] = None
        self.decoction_amt: Optional[Text] = None
        self.version: Optional[int] = None

        @property
        def waterRatio(self):
            raise NotImplementedError('waterRation')