import pandas as pd
import glob
import numpy as np
import os

class Import_Data:
    """ This class imports data from csv files. """

    def __init__(self):
        """ Constructor: Store the imported data. """
        self.data = pd.DataFrame()

    def import_csv(self, file_name='*', folder_name='.', head_row=0, index_col=0, convert_col=True, concat_files=False):
        """ Imports csv file(s) and stores the result in data.

        Note
        ----
        1. If folder exists out of current directory, folder_name should contain correct regex
        2. Assuming there's no file called "\\*.csv"

        Parameters
        ----------
        file_name       : str
            CSV file to be imported. Defaults to '\\*', i.e. all csv files in the folder.
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

        """
        if isinstance(file_name, str) and isinstance(folder_name, str):
            try:
                self.data = self._load_csv(file_name, folder_name, head_row, index_col, convert_col, concat_files)
            except Exception as e:
                raise e
        elif isinstance(file_name, list) and isinstance(folder_name, str):
            for i, file in enumerate(file_name):
                if isinstance(head_row, list):
                    _head_row = head_row[i]
                else:
                    _head_row = head_row
                if isinstance(index_col, list):
                    _index_col = index_col[i]
                else:
                    _index_col = index_col
                try:
                    data_tmp = self._load_csv(file, folder_name, _head_row, _index_col, convert_col, concat_files)
                    if concat_files:
                        self.data = self.data.append(data_tmp, ignore_index=False, verify_integrity=False)
                    else:
                        self.data = self.data.join(data_tmp, how='outer')
                except Exception as e:
                    raise e
        else:
            raise NotImplementedError("Filename and Folder name can't both be of type list.")

    def _load_csv(self, file_name, folder_name, head_row, index_col, convert_col, concat_files):
        """ Load single csv file.

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

        """
        if file_name == '*':
            if not os.path.isdir(folder_name):
                raise OSError('Folder does not exist.')
            else:
                file_name_list = sorted(glob.glob(folder_name + '*.csv'))
                if not file_name_list:
                    raise OSError('Either the folder does not contain any csv files or invalid folder provided.')
                else:
                    self.import_csv(file_name=file_name_list, head_row=head_row, index_col=index_col, convert_col=convert_col, concat_files=concat_files)
                    return self.data
        elif not os.path.isdir(folder_name):
            raise OSError('Folder does not exist.')
        else:
            path = os.path.join(folder_name, file_name)
            if head_row > 0:
                data = pd.read_csv(path, index_col=index_col, skiprows=[i for i in range(head_row - 1)])
            else:
                data = pd.read_csv(path, index_col=index_col)
            try:
                data.index = pd.to_datetime(data.index, format='%m/%d/%y %H:%M')
            except:
                data.index = pd.to_datetime(data.index, dayfirst=False, infer_datetime_format=True)
        if convert_col:
            for col in data.columns:
                if data[col].dtype != np.number:
                    data[col] = pd.to_numeric(data[col], errors='coerce')
        return data