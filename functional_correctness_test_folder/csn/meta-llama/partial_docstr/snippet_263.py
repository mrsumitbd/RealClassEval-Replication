
import pandas as pd
import glob
import os


class Import_Data:

    def __init__(self):
        ''' Constructor.
        This class stores the imported data.
        '''
        self.data = None

    def import_csv(self, file_name='*', folder_name='.', head_row=0, index_col=0, convert_col=True, concat_files=False):
        self.data = self._load_csv(
            file_name, folder_name, head_row, index_col, convert_col, concat_files)
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
        file_path = os.path.join(folder_name, file_name)
        files = glob.glob(file_path)

        if not files:
            raise FileNotFoundError(f"No files found matching {file_path}")

        dfs = []
        for file in files:
            df = pd.read_csv(file, header=head_row, usecols=lambda x: x not in [f'Unnamed: {i}' for i in range(index_col)],
                             na_values=['NA'], parse_dates=False)
            if convert_col:
                df = df.apply(pd.to_numeric, errors='ignore')
            dfs.append(df)

        if concat_files:
            result_df = pd.concat(dfs, ignore_index=True)
        else:
            result_df = dfs[0] if dfs else pd.DataFrame()

        return result_df
