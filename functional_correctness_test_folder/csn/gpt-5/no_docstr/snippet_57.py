import numpy as np


class Surv:

    @staticmethod
    def from_arrays(event, time, name_event=None, name_time=None):
        '''Create structured array from event indicator and time arrays.
        Parameters
        ----------
        event : array-like, shape=(n_samples,)
            Event indicator. A boolean array or array with values 0/1,
            where ``True`` or 1 indicates an event and ``False`` or 0
            indicates right-censoring.
        time : array-like, shape=(n_samples,)
            Observed time. Time to event or time of censoring.
        name_event : str, optional, default: 'event'
            Name of the event field in the structured array.
        name_time : str, optional, default: 'time'
            Name of the observed time field in the structured array.
        Returns
        -------
        y : numpy.ndarray
            A structured array with two fields. The first field is a boolean
            where ``True`` indicates an event and ``False`` indicates right-censoring.
            The second field is a float with the time of event or time of censoring.
            The names of the fields are set to the values of `name_event` and `name_time`.
        Examples
        --------
        >>> from sksurv.util import Surv
        >>>
        >>> y = Surv.from_arrays(event=[True, False, True],
        ...                      time=[10, 25, 15])
        >>> y
        array([( True, 10.), (False, 25.), ( True, 15.)],
            dtype=[('event', '?'), ('time', '<f8')])
        >>> y['event']
        array([ True, False,  True])
        >>> y['time']
        array([10., 25., 15.])
        '''
        name_event = 'event' if name_event is None else str(name_event)
        name_time = 'time' if name_time is None else str(name_time)

        ev = np.asarray(event)
        tm = np.asarray(time)

        if ev.ndim != 1 or tm.ndim != 1:
            raise ValueError("event and time must be one-dimensional arrays.")
        if ev.shape[0] != tm.shape[0]:
            raise ValueError("event and time must have the same length.")

        # Convert event to boolean
        if ev.dtype == np.bool_:
            ev_bool = ev
        else:
            if ev.dtype.kind in ('i', 'u'):  # integer types
                unique_vals = np.unique(ev)
                if not np.all(np.isin(unique_vals, [0, 1])):
                    raise ValueError(
                        "event must be boolean or contain only 0/1 values.")
                ev_bool = ev.astype(bool)
            elif ev.dtype.kind == 'f':  # float types
                if not np.all(np.isfinite(ev)):
                    raise ValueError("event contains NaN or infinite values.")
                unique_vals = np.unique(ev)
                if not np.all(np.isin(unique_vals, [0.0, 1.0])):
                    raise ValueError(
                        "event must be boolean or contain only 0/1 values.")
                ev_bool = ev.astype(bool)
            else:
                raise ValueError(
                    "event must be boolean or numeric array with 0/1 values.")

        # Convert time to float
        tm_float = tm.astype(float)
        if not np.all(np.isfinite(tm_float)):
            raise ValueError("time contains NaN or infinite values.")

        dtype = np.dtype([(name_event, np.bool_), (name_time, np.float64)])
        y = np.empty(ev_bool.shape[0], dtype=dtype)
        y[name_event] = ev_bool
        y[name_time] = tm_float
        return y

    @staticmethod
    def from_dataframe(event, time, data):
        '''Create structured array from columns in a pandas DataFrame.
        Parameters
        ----------
        event : str
            Name of the column in ``data`` containing the event indicator.
            It must be a boolean or have values 0/1,
            where ``True`` or 1 indicates an event and ``False`` or 0
            indicates right-censoring.
        time : str
            Name of the column in ``data`` containing the observed time
            (time to event or time of censoring).
        data : pandas.DataFrame
            A DataFrame with columns for event and time.
        Returns
        -------
        y : numpy.ndarray
            A structured array with two fields. The first field is a boolean
            where ``True`` indicates an event and ``False`` indicates right-censoring.
            The second field is a float with the time of event or time of censoring.
            The names of the fields are the respective column names.
        Examples
        --------
        >>> import pandas as pd
        >>> from sksurv.util import Surv
        >>>
        >>> df = pd.DataFrame({
        ...     'status': [True, False, True],
        ...     'followup_time': [10, 25, 15],
        ... })
        >>> y = Surv.from_dataframe(
        ...     event='status', time='followup_time', data=df,
        ... )
        >>> y
        array([( True, 10.), (False, 25.), ( True, 15.)],
            dtype=[('status', '?'), ('followup_time', '<f8')])
        >>> y['status']
        array([ True, False,  True])
        >>> y['followup_time']
        array([10., 25., 15.])
        '''
        if not hasattr(data, "__getitem__"):
            raise TypeError(
                "data must be a pandas DataFrame-like object supporting column access.")

        if event not in data or time not in data:
            raise KeyError("Specified event or time column not found in data.")

        ev_col = data[event]
        tm_col = data[time]

        return Surv.from_arrays(ev_col, tm_col, name_event=event, name_time=time)
