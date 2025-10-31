
import os
import glob
import pandas as pd


class Import_Data:
    ''' This class imports data from csv files. '''

    def __init__(self):
        ''' Constructor: Store the imported data. '''
        self.data = None

    def import_csv(self, file_name='*', folder_name='.', head_row=0, index_col=0, convert_col=True, concat_files=False):
        ''' Imports csv file(s) and stores the result in data. '''
        # Build file pattern
        if file_name == '*':
            pattern = os.path.join(folder_name, '*.csv')
            files = sorted(glob.glob(pattern))
        else:
            pattern = os.path.join(folder_name, file_name)
            files = sorted(glob.glob(pattern))
        if not files:
            self.data = None
            return

        dataframes = []
        for f in files:
            df = self._load_csv(f, '', head_row, index_col,
                                convert_col, concat_files)
            dataframes.append(df)

        if concat_files:
            self.data = pd.concat(dataframes, ignore_index=True)
        else:
            if len(dataframes) == 1:
                self.data = dataframes[0]
            else:
                self.data = dataframes

    def _load_csv(self, file_name, folder_name, head_row, index_col, convert_col, concat_files):
        ''' Load single csv file. '''
        # file_name is full path if called from import_csv
        # folder_name is ignored in this context
        skiprows = head_row
        df = pd.read_csv(file_name, skiprows=skiprows, header=0)
        if index_col > 0:
            # Drop columns from 0 to index_col-1
            cols_to_drop = df.columns[:index_col]
            df = df.drop(cols_to_drop, axis=1)
        if convert_col:
            for col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='ignore')
        return df
