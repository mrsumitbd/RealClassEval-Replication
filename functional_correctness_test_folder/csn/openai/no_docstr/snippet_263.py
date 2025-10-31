
import os
import glob
import pandas as pd


class Import_Data:
    def __init__(self):
        self.data = None

    def import_csv(self, file_name='*', folder_name='.', head_row=0, index_col=0,
                   convert_col=True, concat_files=False):
        """
        Load CSV file(s) from the specified folder.

        Parameters
        ----------
        file_name : str, optional
            File name or glob pattern. Defaults to '*'.
        folder_name : str, optional
            Folder path. Defaults to current directory.
        head_row : int, optional
            Row number to use as header. Defaults to 0.
        index_col : int, optional
            Column number to use as index. Defaults to 0.
        convert_col : bool, optional
            If True, attempt to convert columns to numeric types. Defaults to True.
        concat_files : bool, optional
            If True, concatenate multiple files into a single DataFrame. Defaults to False.

        Returns
        -------
        pd.DataFrame or None
            Loaded DataFrame or None if no files found.
        """
        self.data = self._load_csv(file_name, folder_name, head_row,
                                   index_col, convert_col, concat_files)
        return self.data

    def _load_csv(self, file_name, folder_name, head_row, index_col,
                  convert_col, concat_files):
        # Resolve the full path pattern
        pattern = os.path.join(folder_name, file_name)
        file_list = glob.glob(pattern)

        if not file_list:
            return None

        dfs = []
        for f in file_list:
            try:
                df = pd.read_csv(f, header=head_row, index_col=index_col)
                if convert_col:
                    # Convert each column to numeric if possible
                    for col in df.columns:
                        df[col] = pd.to_numeric(df[col], errors='ignore')
                dfs.append(df)
            except Exception:
                # Skip files that cannot be read
                continue

        if not dfs:
            return None

        if concat_files:
            return pd.concat(dfs, ignore_index=False)
        else:
            # Return the first DataFrame if multiple files but concat not requested
            return dfs[0]
