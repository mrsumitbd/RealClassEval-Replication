import typing as t

class MutexInfo:

    def __init__(self, opt: str, param: str | None=None, present: t.Callable[[dict[str, t.Any]], bool] | None=None) -> None:
        self.option_name = opt
        if param:
            self.param_name = param
        else:
            self.param_name = opt.lstrip('-').replace('-', '_')
        self.is_present_callback = present

    def is_present(self, d: dict[str, t.Any]) -> bool:
        if self.is_present_callback is not None:
            return self.is_present_callback(d)
        val = d.get(self.param_name)
        return bool(val)

    def __str__(self) -> str:
        return self.option_name