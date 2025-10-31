
import os
import glob
import pandas as pd


class Import_Data:
    def __init__(self):
        pass

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
        Public method to import CSV files.

        Parameters
        ----------
        file_name : str, optional
            File pattern to match (default '*', meaning all files).
        folder_name : str, optional
            Directory to search for files (default '.').
        head_row : int, optional
            Row number to use as header (default 0).
        index_col : int or str, optional
            Column to set as index (default 0).
        convert_col : bool, optional
            If True, attempt to convert columns to numeric where possible.
        concat_files : bool, optional
            If True, concatenate all matched files into a single DataFrame.

        Returns
        -------
        pd.DataFrame
            The loaded (and possibly concatenated) DataFrame.
        """
        return self._load_csv(
            file_name, folder_name, head_row, index_col, convert_col, concat_files
        )

    def _load_csv(
        self,
        file_name,
        folder_name,
        head_row,
        index_col,
        convert_col,
        concat_files,
    ):
        # Resolve the file pattern
        pattern = os.path.join(folder_name, file_name)
        files = glob.glob(pattern)

        if not files:
            raise FileNotFoundError(f"No files matched pattern: {pattern}")

        dfs = []
        for f in files:
            try:
                df = pd.read_csv(
                    f,
                    header=head_row,
                    index_col=index_col,
                    dtype=str,  # read as string first to allow conversion
                )
            except Exception as e:
                raise ValueError(f"Error reading {f}: {e}")

            if convert_col:
                # Attempt to convert each column to numeric where possible
                for col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors="ignore")

            dfs.append(df)

        if concat_files:
            # Concatenate along rows, aligning columns
            result = pd.concat(dfs, axis=0, ignore_index=False, sort=False)
        else:
            # Return the first DataFrame if not concatenating
            result = dfs[0]

        return result
