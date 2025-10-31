import warnings

class _Smoother:
    """
    This is a helper class that implements things that all smoothers should do.
    Right now, the only thing that we need to propagate is the by_col function.

    TBQH, most of these smoothers should be functions, not classes (aside from
    maybe headbanging triples), since they're literally only inits + one
    attribute.
    """

    def __init__(self):
        pass

    @classmethod
    def by_col(cls, df, e, b, inplace=False, **kwargs):
        """
        Compute smoothing by columns in a dataframe.

        Parameters
        -----------
        df      :  pandas.DataFrame
                   a dataframe containing the data to be smoothed
        e       :  string or list of strings
                   the name or names of columns containing event variables to be
                   smoothed
        b       :  string or list of strings
                   the name or names of columns containing the population
                   variables to be smoothed
        inplace :  bool
                   a flag denoting whether to output a copy of `df` with the
                   relevant smoothed columns appended, or to append the columns
                   directly to `df` itself.
        **kwargs:  optional keyword arguments
                   optional keyword options that are passed directly to the
                   smoother.

        Returns
        ---------
        a copy of `df` containing the columns. Or, if `inplace`, this returns
        None, but implicitly adds columns to `df`.
        """
        msg = 'The `.by_col()` methods are deprecated and will be removed in a future version of `esda`.'
        warnings.warn(msg, FutureWarning, stacklevel=True)
        if not inplace:
            new = df.copy()
            cls.by_col(new, e, b, inplace=True, **kwargs)
            return new
        if isinstance(e, str):
            e = [e]
        if isinstance(b, str):
            b = [b]
        if len(b) == 1 and len(e) > 1:
            b = b * len(e)
        try:
            assert len(e) == len(b)
        except AssertionError:
            raise ValueError('There is no one-to-one mapping between event variable and population at risk variable!') from None
        for ei, bi in zip(e, b, strict=True):
            ename = ei
            bname = bi
            ei = df[ename]
            bi = df[bname]
            outcol = '_'.join(('-'.join((ename, bname)), cls.__name__.lower()))
            df[outcol] = cls(ei, bi, **kwargs).r