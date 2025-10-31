
import os
import pandas as pd
import glob


class Import_Data:
    ''' This class imports data from csv files. '''

    def __init__(self):
        ''' Constructor: Store the imported data. '''
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
        if file_name == '*':
            file_pattern = os.path.join(folder_name, '*.csv')
            file_list = glob.glob(file_pattern)
        else:
            file_list = [os.path.join(folder_name, file_name)]

        if not file_list:
            raise FileNotFoundError(
                "No CSV files found matching the given pattern.")

        if concat_files:
            self.data = pd.concat([self._load_csv(f, folder_name, head_row, index_col,
                                  convert_col, concat_files) for f in file_list], ignore_index=True)
        else:
            self.data = self._load_csv(
                file_list[0], folder_name, head_row, index_col, convert_col, concat_files)

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
        df = pd.read_csv(file_name, skiprows=head_row, usecols=lambda column: column not in range(
            index_col), header=head_row)
        if convert_col:
            df = df.apply(pd.to_numeric, errors='ignore')
        return df
