
import numpy as np


class Surv:
    '''A helper class to create a structured array for survival analysis.
    This class provides helper functions to create a structured array that
    encapsulates the event indicator and the observed time. The resulting
    structured array is the recommended format for the ``y`` argument in
    scikit-survival's estimators.
    '''
    @staticmethod
    def from_arrays(event, time, name_event=None, name_time=None):
        '''Create structured array from event indicator and time arrays.'''
        if name_event is None:
            name_event = 'event'
        if name_time is None:
            name_time = 'time'

        event_arr = np.asarray(event)
        time_arr = np.asarray(time)

        if event_arr.dtype != np.bool_:
            # Accept 0/1 or True/False, convert to bool
            event_arr = event_arr.astype(bool)

        time_arr = time_arr.astype(float)

        dtype = [(name_event, '?'), (name_time, '<f8')]
        y = np.empty(event_arr.shape[0], dtype=dtype)
        y[name_event] = event_arr
        y[name_time] = time_arr
        return y

    @staticmethod
    def from_dataframe(event, time, data):
        '''Create structured array from columns in a pandas DataFrame.'''
        event_arr = data[event]
        time_arr = data[time]

        # Convert event to bool if not already
        if event_arr.dtype != np.bool_:
            event_arr = event_arr.astype(bool)
        else:
            event_arr = event_arr.values

        time_arr = time_arr.astype(float).values

        dtype = [(event, '?'), (time, '<f8')]
        y = np.empty(len(data), dtype=dtype)
        y[event] = event_arr
        y[time] = time_arr
        return y
