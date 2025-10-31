from sklearn.utils.validation import check_array, check_consistent_length
import numpy as np
import pandas as pd

class Surv:
    """A helper class to create a structured array for survival analysis.

    This class provides helper functions to create a structured array that
    encapsulates the event indicator and the observed time. The resulting
    structured array is the recommended format for the ``y`` argument in
    scikit-survival's estimators.
    """

    @staticmethod
    def from_arrays(event, time, name_event=None, name_time=None):
        """Create structured array from event indicator and time arrays.

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
        """
        name_event = name_event or 'event'
        name_time = name_time or 'time'
        if name_time == name_event:
            raise ValueError('name_time must be different from name_event')
        time = np.asanyarray(time, dtype=float)
        y = np.empty(time.shape[0], dtype=[(name_event, bool), (name_time, float)])
        y[name_time] = time
        event = np.asanyarray(event)
        check_consistent_length(time, event)
        if np.issubdtype(event.dtype, np.bool_):
            y[name_event] = event
        else:
            events = np.unique(event)
            events.sort()
            if len(events) != 2:
                raise ValueError('event indicator must be binary')
            if np.all(events == np.array([0, 1], dtype=events.dtype)):
                y[name_event] = event.astype(bool)
            else:
                raise ValueError('non-boolean event indicator must contain 0 and 1 only')
        return y

    @staticmethod
    def from_dataframe(event, time, data):
        """Create structured array from columns in a pandas DataFrame.

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
        """
        if not isinstance(data, pd.DataFrame):
            raise TypeError(f'expected pandas.DataFrame, but got {type(data)!r}')
        return Surv.from_arrays(data.loc[:, event].values, data.loc[:, time].values, name_event=str(event), name_time=str(time))