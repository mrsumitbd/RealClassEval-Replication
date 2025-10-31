
import os
import glob
import pandas as pd


class Import_Data:
    ''' This class imports data from csv files. '''

    def __init__(self):
        # No initialization needed for now
        pass

    def import_csv(self, file_name='*', folder_name='.', head_row=0, index_col=0,
                   convert_col=True, concat_files=False):
        """
        Public method to import CSV files.

        Parameters
        ----------
        file_name : str or list of str, default '*'
            Pattern or specific file name(s) to load. If a list is provided,
            each element is treated as a separate file pattern.
        folder_name : str, default '.'
            Directory where the CSV files are located.
        head_row : int, default 0
            Row number to use as the header.
        index_col : int or str, default 0
            Column to set as index.
        convert_col : bool, default True
            If True, attempt to convert all columns to numeric where possible.
        concat_files : bool, default False
            If True and multiple files are found, concatenate them into a single
            DataFrame. Otherwise, return a list of DataFrames.

        Returns
        -------
        pd.DataFrame or list of pd.DataFrame
            The loaded data.
        """
        return self._load_csv(file_name, folder_name, head_row, index_col,
                              convert_col, concat_files)

    def _load_csv(self, file_name, folder_name, head_row, index_col,
                  convert_col, concat_files):
        # Resolve file patterns
        if isinstance(file_name, str):
            patterns = [file_name]
        else:
            patterns = list(file_name)

        all_files = []
        for pattern in patterns:
            # Build full pattern path
            full_pattern = os.path.join(folder_name, pattern)
            matched = glob.glob(full_pattern)
            if not matched:
                # If pattern is a specific file and doesn't exist, raise error
                if os.path.isfile(full_pattern):
                    matched = [full_pattern]
                else:
                    continue
            all_files.extend(matched)

        if not all_files:
            raise FileNotFoundError(
                f"No CSV files found for pattern(s) {patterns} in {folder_name}")

        dfs = []
        for f in all_files:
            try:
                df = pd.read_csv(f, header=head_row, index_col=index_col)
            except Exception as e:
                raise ValueError(f"Error reading {f}: {e}")

            if convert_col:
                # Convert all columns to numeric where possible
                for col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='ignore')

            dfs.append(df)

        if concat_files:
            # Concatenate along rows, aligning columns
            result = pd.concat(dfs, axis=0, ignore_index=False)
            return result
        else:
            return dfs
