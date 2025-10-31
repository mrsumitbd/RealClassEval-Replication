
import pandas as pd
import os
import glob


class Import_Data:

    def __init__(self):
        ''' Constructor.
        This class stores the imported data.
        '''
        self.data = pd.DataFrame()

    def import_csv(self, file_name='*', folder_name='.', head_row=0, index_col=0, convert_col=True, concat_files=False):
        if file_name == '*':
            files = glob.glob(os.path.join(folder_name, '*.csv'))
            for file in files:
                self._load_csv(file, folder_name, head_row,
                               index_col, convert_col, concat_files)
        else:
            self._load_csv(file_name, folder_name, head_row,
                           index_col, convert_col, concat_files)

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
        file_path = os.path.join(folder_name, file_name)
        df = pd.read_csv(file_path, header=head_row, index_col=index_col)
        if convert_col:
            df = df.apply(pd.to_numeric, errors='ignore')
        if concat_files:
            self.data = pd.concat([self.data, df], ignore_index=True)
        else:
            self.data = df
        return self.data
