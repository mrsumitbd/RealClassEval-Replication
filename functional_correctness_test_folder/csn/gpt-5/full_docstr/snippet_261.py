import os
import glob
import pandas as pd


class Import_Data:
    ''' This class imports data from csv files. '''

    def __init__(self):
        ''' Constructor: Store the imported data. '''
        self.data = None
        self.files_loaded = []

    def import_csv(self, file_name='*', folder_name='.', head_row=0, index_col=0, convert_col=True, concat_files=False):
        ''' Imports csv file(s) and stores the result in data.
        Note
        ----
        1. If folder exists out of current directory, folder_name should contain correct regex
        2. Assuming there's no file called "\*.csv"
        Parameters
        ----------
        file_name       : str
            CSV file to be imported. Defaults to '\*', i.e. all csv files in the folder.
        folder_name     : str
            Folder where file resides. Defaults to '.', i.e. current directory.
        head_row        : int
            Skips all rows from 0 to head_row-1
        index_col       : int
            Skips all columns from 0 to index_col-1
        convert_col     : bool
            Convert columns to numeric type
        concat_files    : bool
            Appends data from files to result dataframe
        '''
        # Build glob pattern supporting wildcards in both folder and file
        if file_name.endswith('.csv'):
            pattern = os.path.join(folder_name, file_name)
        else:
            pattern = os.path.join(folder_name, f'{file_name}.csv')

        file_list = sorted(glob.glob(pattern))
        if not file_list:
            raise FileNotFoundError(f'No CSV files match pattern: {pattern}')

        self.files_loaded = file_list[:]

        if concat_files:
            frames = [
                self._load_csv(f, folder_name=None, head_row=head_row, index_col=index_col,
                               convert_col=convert_col, concat_files=True)
                for f in file_list
            ]
            self.data = pd.concat(frames, ignore_index=True, sort=False)
        else:
            data_dict = {}
            for f in file_list:
                df = self._load_csv(f, folder_name=None, head_row=head_row, index_col=index_col,
                                    convert_col=convert_col, concat_files=False)
                data_dict[os.path.basename(f)] = df
            # If only one file and not concatenating, store the DataFrame directly
            self.data = next(iter(data_dict.values())) if len(
                data_dict) == 1 else data_dict

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
        # Resolve full path if folder_name provided; otherwise assume file_name is a full path/pattern
        path = os.path.join(
            folder_name, file_name) if folder_name else file_name

        # Read CSV, skipping leading rows; treat the first remaining row as header
        df = pd.read_csv(path, header=0, skiprows=head_row)

        # Drop the first index_col columns (keep columns from index_col onward)
        if index_col and index_col > 0:
            df = df.iloc[:, index_col:].copy()

        # Optionally attempt to convert columns to numeric where possible
        if convert_col and not df.empty:
            for col in df.columns:
                # Try converting; if conversion fails for any value, keep original
                converted = pd.to_numeric(df[col], errors='ignore')
                df[col] = converted

        return df
