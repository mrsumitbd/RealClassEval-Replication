import os
import glob
import pandas as pd


class Import_Data:
    ''' This class imports data from csv files '''

    def __init__(self):
        ''' Constructor.
        This class stores the imported data.
        '''
        self.data = None

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
        # Build glob pattern
        fn = file_name
        if fn == '*' or '*' in fn:
            pattern = fn if fn.endswith('.csv') or fn.endswith(
                '*.csv') else (fn + '.csv')
        else:
            pattern = fn if fn.lower().endswith('.csv') else (fn + '.csv')

        search_pattern = os.path.join(folder_name, pattern)
        file_list = sorted(glob.glob(search_pattern))

        if not file_list:
            raise FileNotFoundError(
                f"No CSV files matched pattern: {search_pattern}")

        if concat_files:
            frames = [
                self._load_csv(f, folder_name='', head_row=head_row, index_col=index_col,
                               convert_col=convert_col, concat_files=concat_files)
                for f in file_list
            ]
            result = pd.concat(
                frames, ignore_index=True) if frames else pd.DataFrame()
            self.data = result
            return result
        else:
            # If only one file, store DataFrame directly, else store dict of DataFrames keyed by file path
            if len(file_list) == 1:
                df = self._load_csv(file_list[0], folder_name='', head_row=head_row, index_col=index_col,
                                    convert_col=convert_col, concat_files=concat_files)
                self.data = df
                return df
            else:
                data_dict = {}
                for f in file_list:
                    data_dict[f] = self._load_csv(f, folder_name='', head_row=head_row, index_col=index_col,
                                                  convert_col=convert_col, concat_files=concat_files)
                self.data = data_dict
                return data_dict

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
        # Determine full path
        if folder_name:
            path = os.path.join(folder_name, file_name)
        else:
            path = file_name

        # Read CSV: skip first head_row lines; treat the next line as header
        df = pd.read_csv(path, header=0, skiprows=head_row)

        # Drop the first index_col columns
        if index_col and index_col > 0:
            df = df.iloc[:, index_col:]

        # Convert columns to numeric where possible
        if convert_col and not df.empty:
            for col in df.columns:
                # Try numeric conversion; if fails, leave as-is
                converted = pd.to_numeric(df[col], errors='ignore')
                df[col] = converted

        return df
