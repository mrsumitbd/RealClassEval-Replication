
import numpy as np
import pandas as pd


class Surv:

    @staticmethod
    def from_arrays(event, time, name_event='event', name_time='time'):
        event = np.array(event, dtype=bool)
        time = np.array(time, dtype=float)
        dtype = [(name_event, '?'), (name_time, '<f8')]
        return np.array(list(zip(event, time)), dtype=dtype)

    @staticmethod
    def from_dataframe(event, time, data):
        event_col = data[event].values.astype(bool)
        time_col = data[time].values.astype(float)
        dtype = [(event, '?'), (time, '<f8')]
        return np.array(list(zip(event_col, time_col)), dtype=dtype)
