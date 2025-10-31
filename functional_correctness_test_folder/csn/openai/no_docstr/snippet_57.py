
import numpy as np
import pandas as pd


class Surv:
    @staticmethod
    def from_arrays(event, time, name_event="event", name_time="time"):
        """Create structured array from event indicator and time arrays."""
        event_arr = np.asarray(event, dtype=bool)
        time_arr = np.asarray(time, dtype=float)

        if event_arr.shape != time_arr.shape:
            raise ValueError("event and time must have the same shape")

        dtype = [(name_event, "?"), (name_time, "<f8")]
        y = np.empty(event_arr.shape[0], dtype=dtype)
        y[name_event] = event_arr
        y[name_time] = time_arr
        return y

    @staticmethod
    def from_dataframe(event, time, data):
        """Create structured array from columns in a pandas DataFrame."""
        if not isinstance(data, pd.DataFrame):
            raise TypeError("data must be a pandas DataFrame")

        if event not in data.columns:
            raise KeyError(f"Column '{event}' not found in DataFrame")
        if time not in data.columns:
            raise KeyError(f"Column '{time}' not found in DataFrame")

        event_col = data[event].values
        time_col = data[time].values
        return Surv.from_arrays(event_col, time_col, name_event=event, name_time=time)
