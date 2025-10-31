from datetime import datetime, timedelta, timezone

class DumpFormat:

    def __init__(self, template: str, sep: str=',') -> None:
        self.template = template
        self.sep = sep
        self.cols = list((x.strip() for x in template.split(sep)))
        time_gen = (i for i, elt in enumerate(self.cols) if elt == 'time')
        time_index = next(time_gen, None)
        if time_index is not None:
            self.time_index = time_index
        else:
            msg = "Format invalid: must contain 'time'"
            raise ValueError(msg)
        long_gen = (i for i, elt in enumerate(self.cols) if elt == 'longmsg')
        self.msg_index = next(long_gen, None)
        self.splitmsg = slice(18, None)
        if self.msg_index is not None:
            return
        short_gen = (i for i, elt in enumerate(self.cols) if elt == 'shortmsg')
        self.msg_index = next(short_gen, None)
        if self.msg_index is None:
            msg = "Format invalid: must contain either 'longmsg' or 'shortmsg'"
            raise ValueError(msg)
        self.splitmsg = slice(None)

    def get_timestamp(self, line: str) -> datetime:
        elts = line.split(self.sep)
        return datetime.fromtimestamp(float(elts[self.time_index].strip()), timezone.utc)

    def get_msg(self, line: str) -> str:
        elts = line.split(self.sep)
        return elts[self.msg_index][self.splitmsg].strip()