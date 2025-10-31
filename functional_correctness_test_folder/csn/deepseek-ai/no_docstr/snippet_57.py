
import numpy as np
import pandas as pd


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
        if name_event is None:
            name_event = 'event'
        if name_time is None:
            name_time = 'time'

        event = np.asarray(event, dtype=bool)
        time = np.asarray(time, dtype=np.float64)

        y = np.empty(len(event), dtype=[(name_event, '?'), (name_time, '<f8')])
        y[name_event] = event
        y[name_time] = time

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
        event_data = data[event].values
        time_data = data[time].values

        y = np.empty(len(event_data), dtype=[(event, '?'), (time, '<f8')])
        y[event] = event_data.astype(bool)
        y[time] = time_data.astype(np.float64)

        return y
