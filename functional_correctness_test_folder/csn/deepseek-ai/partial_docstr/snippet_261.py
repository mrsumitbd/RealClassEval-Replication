
import pandas as pd
import os
import glob


class Import_Data:
    ''' This class imports data from csv files. '''

    def __init__(self):
        self.data = None

    def import_csv(self, file_name='*', folder_name='.', head_row=0, index_col=0, convert_col=True, concat_files=False):
        return self._load_csv(file_name, folder_name, head_row, index_col, convert_col, concat_files)

    def _load_csv(self, file_name, folder_name, head_row, index_col, convert_col, concat_files):
        if not os.path.isdir(folder_name):
            raise ValueError(f"Folder '{folder_name}' does not exist.")

        full_path = os.path.join(folder_name, file_name + '.csv')
        csv_files = glob.glob(full_path)

        if not csv_files:
            raise FileNotFoundError(
                f"No CSV files found matching '{file_name}' in '{folder_name}'.")

        dfs = []
        for csv_file in csv_files:
            df = pd.read_csv(csv_file, header=head_row, index_col=index_col)
            if convert_col:
                for col in df.columns:
                    try:
                        df[col] = pd.to_numeric(df[col])
                    except ValueError:
                        pass
            dfs.append(df)

        if concat_files:
            self.data = pd.concat(dfs, axis=0)
        else:
            if len(dfs) == 1:
                self.data = dfs[0]
            else:
                self.data = dfs

        return self.data
