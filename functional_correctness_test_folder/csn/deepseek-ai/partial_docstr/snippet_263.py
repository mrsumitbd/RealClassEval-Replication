
import pandas as pd
import os


class Import_Data:

    def __init__(self):
        ''' Constructor.
        This class stores the imported data.
        '''
        self.data = None

    def import_csv(self, file_name='*', folder_name='.', head_row=0, index_col=0, convert_col=True, concat_files=False):
        ''' Import CSV file(s) into a DataFrame.

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
        '''
        self.data = self._load_csv(
            file_name, folder_name, head_row, index_col, convert_col, concat_files)

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
        if file_name == '*':
            csv_files = [f for f in os.listdir(
                folder_name) if f.endswith('.csv')]
            if not csv_files:
                raise FileNotFoundError(
                    "No CSV files found in the specified folder.")
            dfs = []
            for csv_file in csv_files:
                file_path = os.path.join(folder_name, csv_file)
                df = pd.read_csv(file_path, skiprows=head_row,
                                 index_col=index_col)
                if convert_col:
                    df = df.apply(pd.to_numeric, errors='ignore')
                if concat_files:
                    dfs.append(df)
                else:
                    return df
            return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()
        else:
            file_path = os.path.join(folder_name, file_name)
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File {file_path} not found.")
            df = pd.read_csv(file_path, skiprows=head_row, index_col=index_col)
            if convert_col:
                df = df.apply(pd.to_numeric, errors='ignore')
            return df
