
import numpy as np


class Surv:

    @staticmethod
    def from_arrays(event, time, name_event=None, name_time=None):
        if name_event is None:
            name_event = 'event'
        if name_time is None:
            name_time = 'time'
        event_arr = np.asarray(event)
        time_arr = np.asarray(time)
        if event_arr.shape != time_arr.shape:
            raise ValueError("event and time must have the same shape")
        # Convert event to boolean
        if event_arr.dtype == bool:
            event_bool = event_arr
        else:
            event_bool = (event_arr == 1) | (event_arr == True)
        time_float = time_arr.astype(float)
        dtype = [(name_event, '?'), (name_time, '<f8')]
        structured = np.empty(event_bool.shape[0], dtype=dtype)
        structured[name_event] = event_bool
        structured[name_time] = time_float
        return structured

    @staticmethod
    def from_dataframe(event, time, data):
        import pandas as pd
        if not isinstance(data, pd.DataFrame):
            raise ValueError("data must be a pandas DataFrame")
        event_arr = data[event]
        time_arr = data[time]
        # Convert event to boolean
        if event_arr.dtype == bool:
            event_bool = event_arr.values
        else:
            event_bool = (event_arr == 1) | (event_arr == True)
        time_float = time_arr.values.astype(float)
        dtype = [(event, '?'), (time, '<f8')]
        structured = np.empty(len(data), dtype=dtype)
        structured[event] = event_bool
        structured[time] = time_float
        return structured
