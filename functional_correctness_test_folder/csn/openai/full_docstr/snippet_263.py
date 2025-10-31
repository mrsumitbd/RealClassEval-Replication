
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

    def import_csv(self, file_name='*', folder_name='.', head_row=0, index_col=0,
                   convert_col=True, concat_files=False):
        ''' Imports csv file(s) and stores the result in data.
        Note
        ----
        1. If folder exists out of current directory, folder_name should contain correct regex
        2. Assuming there's no file called "*.csv"
        Parameters
        ----------
        file_name       : str
            CSV file to be imported. Defaults to '*', i.e. all csv files in the folder.
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
        # Resolve file pattern
        pattern = os.path.join(folder_name, file_name if file_name.endswith(
            '.csv') else f"{file_name}.csv")
        files = glob.glob(pattern)

        if not files:
            raise FileNotFoundError(
                f"No CSV files found for pattern: {pattern}")

        # If only one file or concat_files is False, load the first file only
        if not concat_files or len(files) == 1:
            self.data = self._load_csv(files[0], folder_name, head_row, index_col,
                                       convert_col, concat_files)
        else:
            dfs = []
            for f in files:
                df = self._load_csv(f, folder_name, head_row, index_col,
                                    convert_col, concat_files)
                dfs.append(df)
            self.data = pd.concat(dfs, ignore_index=True)

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
        # Build full path
        full_path = os.path.join(folder_name, file_name) if not os.path.isabs(
            file_name) else file_name

        # Read CSV
        df = pd.read_csv(full_path, skiprows=head_row, index_col=index_col)

        # Convert columns to numeric if requested
        if convert_col:
            df = df.apply(pd.to_numeric, errors='ignore')

        return df
