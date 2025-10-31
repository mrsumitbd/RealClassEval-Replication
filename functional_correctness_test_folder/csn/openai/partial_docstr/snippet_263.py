
import os
import glob
import pandas as pd


class Import_Data:
    def __init__(self):
        """Constructor.
        This class stores the imported data.
        """
        self.data = pd.DataFrame()

    def import_csv(
        self,
        file_name="*",
        folder_name=".",
        head_row=0,
        index_col=0,
        convert_col=True,
        concat_files=False,
    ):
        """
        Import CSV files from a folder.

        Parameters
        ----------
        file_name : str, optional
            CSV file to be imported. Defaults to '*' - all csv files in the folder.
        folder_name : str, optional
            Folder where file resides. Defaults to '.' - current directory.
        head_row : int, optional
            Skips all rows from 0 to head_row-1
        index_col : int, optional
            Skips all columns from 0 to index_col-1
        convert_col : bool, optional
            Convert columns to numeric type
        concat_files : bool, optional
            Appends data from files to result dataframe

        Returns
        -------
        pd.DataFrame
            Dataframe containing csv data
        """
        # Resolve folder path
        folder_path = os.path.abspath(folder_name)

        # Determine file list
        if file_name == "*":
            pattern = os.path.join(folder_path, "*.csv")
            files = sorted(glob.glob(pattern))
        else:
            files = [os.path.join(folder_path, file_name)]

        if not files:
            self.data = pd.DataFrame()
            return self.data

        # Load files
        dfs = []
        for f in files:
            df = self._load_csv(
                f, folder_path, head_row, index_col, convert_col, concat_files
            )
            if not df.empty:
                dfs.append(df)

        if not dfs:
            self.data = pd.DataFrame()
            return self.data

        if concat_files:
            self.data = pd.concat(dfs, ignore_index=True)
        else:
            self.data = dfs[0]

        return self.data

    def _load_csv(
        self,
        file_name,
        folder_name,
        head_row,
        index_col,
        convert_col,
        concat_files,
    ):
        """
        Load single csv file.

        Parameters
        ----------
        file_name : str
            CSV file to be imported. Defaults to '*' - all csv files in the folder.
        folder_name : str
            Folder where file resides. Defaults to '.' - current directory.
        head_row : int
            Skips all rows from 0 to head_row-1
        index_col : int
            Skips all columns from 0 to index_col-1
        convert_col : bool
            Convert columns to numeric type
        concat_files : bool
            Appends data from files to result dataframe

        Returns
        -------
        pd.DataFrame
            Dataframe containing csv data
        """
        # Build full path
        full_path = os.path.join(folder_name, file_name)

        # Read CSV
        try:
            df = pd.read_csv(
                full_path,
                skiprows=range(head_row),
                header=0,
                dtype=str,  # read as string first
            )
        except Exception:
            return pd.DataFrame()

        # Drop columns before index_col
        if index_col > 0:
            df = df.iloc[:, index_col:]

        # Convert columns to numeric if requested
        if convert_col:
            df = df.apply(pd.to_numeric, errors="coerce")

        return df
