from pyinstrument.low_level.types import TimerType
from typing import Any, Callable, List, Optional, Type
from pyinstrument.low_level.pyi_timing_thread_python import pyi_timing_thread_get_time, pyi_timing_thread_subscribe, pyi_timing_thread_unsubscribe
import types
import timeit
import contextvars

class PythonStatProfiler:
    await_stack: list[str]
    timing_thread_subscription: int | None = None

    def __init__(self, target: Callable[[types.FrameType, str, Any], Any], interval: float, context_var: contextvars.ContextVar[object | None] | None, timer_type: TimerType, timer_func: Callable[[], float] | None):
        self.target = target
        self.interval = interval
        if context_var:
            if not isinstance(context_var, contextvars.ContextVar):
                raise TypeError('not a context var')
        self.context_var = context_var
        self.timer_type = timer_type
        if timer_type == 'walltime':
            self.get_time = timeit.default_timer
        elif timer_type == 'walltime_thread':
            self.get_time = pyi_timing_thread_get_time
            self.timing_thread_subscription = pyi_timing_thread_subscribe(interval)
        elif timer_type == 'timer_func':
            if timer_func is None:
                raise TypeError('timer_func must be provided for timer_func timer_type')
            self.get_time = timer_func
        else:
            raise ValueError(f"invalid timer_type '{timer_type}'")
        self.last_invocation = self.get_time()
        self.last_context_var_value = context_var.get() if context_var else None
        self.await_stack = []

    def __del__(self):
        if self.timing_thread_subscription is not None:
            pyi_timing_thread_unsubscribe(self.timing_thread_subscription)

    def profile(self, frame: types.FrameType, event: str, arg: Any):
        now = self.get_time()
        if self.context_var:
            context_var_value = self.context_var.get()
            last_context_var_value = self.last_context_var_value
            if context_var_value is not last_context_var_value:
                context_change_frame = frame.f_back if event == 'call' else frame
                assert context_change_frame is not None
                self.target(context_change_frame, 'context_changed', (context_var_value, last_context_var_value, self.await_stack))
                self.last_context_var_value = context_var_value
            if event == 'return' and frame.f_code.co_flags & 128:
                self.await_stack.append(get_frame_info(frame))
            else:
                self.await_stack.clear()
        if now < self.last_invocation + self.interval:
            return
        self.last_invocation = now
        return self.target(frame, event, arg)