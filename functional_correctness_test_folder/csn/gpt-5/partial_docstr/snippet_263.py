import os
import glob
import pandas as pd


class Import_Data:

    def __init__(self):
        ''' Constructor.
        This class stores the imported data.
        '''
        self.data = {}
        self.concatenated = None
        self.files = []

    def import_csv(self, file_name='*', folder_name='.', head_row=0, index_col=0, convert_col=True, concat_files=False):
        # Resolve file paths
        folder = os.path.abspath(folder_name)
        if file_name == '*' or '*' in file_name or '?' in file_name:
            pattern = file_name if file_name != '*' else '*.csv'
            paths = sorted(glob.glob(os.path.join(folder, pattern)))
        else:
            candidate = os.path.join(folder, file_name)
            if os.path.isdir(candidate):
                paths = sorted(glob.glob(os.path.join(candidate, '*.csv')))
            else:
                paths = [candidate]

        paths = [p for p in paths if os.path.isfile(
            p) and p.lower().endswith('.csv')]
        if not paths:
            raise FileNotFoundError(
                "No CSV files found with the given parameters.")

        self.files = paths
        self.data = {}
        frames = []

        for p in paths:
            df = self._load_csv(
                file_name=os.path.basename(p),
                folder_name=os.path.dirname(p),
                head_row=head_row,
                index_col=index_col,
                convert_col=convert_col,
                concat_files=concat_files
            )
            self.data[p] = df
            frames.append(df)

        if concat_files or len(frames) == 1:
            self.concatenated = pd.concat(frames, axis=0, ignore_index=True) if len(
                frames) > 1 else frames[0].copy()
            return self.concatenated

        return self.data

    def _load_csv(self, file_name, folder_name, head_row, index_col, convert_col, concat_files):
        ''' Load single csv file.
        Parameters
        ----------
        file_name       : str
            CSV file to be imported. Defaults to '*' - all csv files in the folder.
        folder_name     : str
            Folder where file resides. Defaults to '.' - current directory.
        head_row        : int
            Skips all rows from 0 to head_row-1
        index_col       : int
            Skips all columns from 0 to index_col-1
        convert_col     : bool
            Convert columns to numeric type
        concat_files    : bool
            Appends data from files to result dataframe
        Returns
        -------
        pd.DataFrame()
            Dataframe containing csv data
        '''
        path = os.path.join(folder_name, file_name)
        if not os.path.isfile(path):
            raise FileNotFoundError(f"CSV file not found: {path}")

        df = pd.read_csv(
            path, skiprows=head_row if head_row and head_row > 0 else None)

        if index_col and index_col > 0:
            if df.shape[1] <= index_col:
                df = df.iloc[:, 0:0]
            else:
                df = df.iloc[:, index_col:]

        if convert_col and not df.empty:
            for c in df.columns:
                if pd.api.types.is_object_dtype(df[c]):
                    converted = pd.to_numeric(df[c], errors='ignore')
                    df[c] = converted

        return df
