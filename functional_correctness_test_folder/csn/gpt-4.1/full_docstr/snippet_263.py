
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
        self.files = []

    def import_csv(self, file_name='*', folder_name='.', head_row=0, index_col=0, convert_col=True, concat_files=False):
        ''' Imports csv file(s) and stores the result in data. '''
        # Build file pattern
        if file_name == '*':
            pattern = os.path.join(folder_name, '*.csv')
            file_list = sorted(glob.glob(pattern))
        else:
            pattern = os.path.join(folder_name, file_name)
            file_list = sorted(glob.glob(pattern))
        self.files = file_list

        if not file_list:
            self.data = None
            return

        dataframes = []
        for f in file_list:
            df = self._load_csv(f, folder_name, head_row,
                                index_col, convert_col, concat_files)
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
        # Read CSV, skip head_row rows
        df = pd.read_csv(file_name, skiprows=head_row)
        # Drop columns before index_col
        if index_col > 0:
            df = df.iloc[:, index_col:]
        # Convert columns to numeric if requested
        if convert_col:
            for col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='ignore')
        return df
