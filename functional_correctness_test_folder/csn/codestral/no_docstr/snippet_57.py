
import numpy as np
import pandas as pd


class Surv:

    @staticmethod
    def from_arrays(event, time, name_event=None, name_time=None):
        if name_event is None:
            name_event = 'event'
        if name_time is None:
            name_time = 'time'

        event = np.asarray(event, dtype=bool)
        time = np.asarray(time, dtype=float)

        dtype = [(name_event, bool), (name_time, float)]
        y = np.empty(len(event), dtype=dtype)
        y[name_event] = event
        y[name_time] = time

        return y

    @staticmethod
    def from_dataframe(event, time, data):
        event_data = data[event].values
        time_data = data[time].values

        dtype = [(event, bool), (time, float)]
        y = np.empty(len(event_data), dtype=dtype)
        y[event] = event_data
        y[time] = time_data

        return y
