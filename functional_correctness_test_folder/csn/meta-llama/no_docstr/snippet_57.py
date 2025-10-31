
import numpy as np
import pandas as pd


class Surv:

    @staticmethod
    def from_arrays(event, time, name_event='event', name_time='time'):
        event = np.asarray(event, dtype=bool)
        time = np.asarray(time, dtype=float)

        if event.shape != time.shape:
            raise ValueError("event and time must have the same shape")

        y = np.empty(event.shape[0], dtype=[
                     (name_event, bool), (name_time, float)])
        y[name_event] = event
        y[name_time] = time

        return y

    @staticmethod
    def from_dataframe(event, time, data):
        if not isinstance(data, pd.DataFrame):
            raise TypeError("data must be a pandas DataFrame")

        if event not in data.columns or time not in data.columns:
            raise ValueError("event and time must be columns in data")

        event_values = data[event].values
        time_values = data[time].values

        return Surv.from_arrays(event_values, time_values, name_event=event, name_time=time)
