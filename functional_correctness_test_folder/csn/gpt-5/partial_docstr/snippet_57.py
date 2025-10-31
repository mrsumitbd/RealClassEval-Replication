class Surv:
    '''A helper class to create a structured array for survival analysis.
    This class provides helper functions to create a structured array that
    encapsulates the event indicator and the observed time. The resulting
    structured array is the recommended format for the ``y`` argument in
    scikit-survival's estimators.
    '''
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
        import numpy as np

        if name_event is None:
            name_event = "event"
        if name_time is None:
            name_time = "time"

        ev = np.asarray(event)
        tm = np.asarray(time)

        if ev.shape[0] != tm.shape[0]:
            raise ValueError(
                "event and time must have the same number of samples")

        ev_bool = ev.astype(bool, copy=False)
        tm_float = tm.astype(float, copy=False)

        dtype = [(name_event, np.bool_), (name_time, np.float64)]
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
        ev = data[event].to_numpy()
        tm = data[time].to_numpy()
        return Surv.from_arrays(ev, tm, name_event=event, name_time=time)
