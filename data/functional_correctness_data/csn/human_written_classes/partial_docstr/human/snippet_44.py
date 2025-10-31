from pyspark.sql import DataFrame
from typing import Any, List, Optional

class MissingnoBarSparkPatch:
    """
    Technical Debt :
    This is a monkey patching object that allows usage of the library missingno as is for spark dataframes.
    This is because missingno library's bar function always applies a isnull().sum() on dataframes in the visualisation
    function, instead of allowing just values counts as an entry point. Thus, in order to calculate the
    missing values dataframe in spark, we compute it first, then wrap it in this MissingnoBarSparkPatch object which
    will be unwrapped by missingno and return the pre-computed value counts.
    The best fix to this currently terrible patch is to submit a PR to missingno to separate preprocessing function
    (compute value counts from df) and visualisation functions such that we can call the visualisation directly.
    Unfortunately, the missingno library people have not really responded to our issues on gitlab.
    See https://github.com/ResidentMario/missingno/issues/119.
    We could also fork the missingno library and implement some of the code in our database, but that feels
    like bad practice as well.
    """

    def __init__(self, df: DataFrame, columns: List[str]=None, original_df_size: int=None):
        self.df = df
        self.columns = columns
        self.original_df_size = original_df_size

    def isnull(self) -> Any:
        """
        This patches the .isnull().sum() function called by missingno library
        """
        return self

    def sum(self) -> DataFrame:
        """
        This patches the .sum() function called by missingno library
        """
        return self.df

    def __len__(self) -> Optional[int]:
        """
        This patches the len(df) function called by missingno library
        """
        return self.original_df_size