
import pandas as pd
import os
import glob


class Import_Data:

    def __init__(self):
        self.data = None

    def import_csv(self, file_name='*', folder_name='.', head_row=0, index_col=0, convert_col=True, concat_files=False):
        self.data = self._load_csv(
            file_name, folder_name, head_row, index_col, convert_col, concat_files)
        return self.data

    def _load_csv(self, file_name, folder_name, head_row, index_col, convert_col, concat_files):
        if not os.path.isdir(folder_name):
            raise ValueError(f"Folder '{folder_name}' does not exist.")

        full_path = os.path.join(folder_name, file_name)
        csv_files = glob.glob(full_path)

        if not csv_files:
            raise ValueError(
                f"No files found matching pattern '{file_name}' in folder '{folder_name}'.")

        dfs = []
        for csv_file in csv_files:
            df = pd.read_csv(csv_file, header=head_row, index_col=index_col)
            if convert_col:
                df = df.apply(pd.to_numeric, errors='ignore')
            dfs.append(df)

        if concat_files and len(dfs) > 1:
            combined_df = pd.concat(dfs, axis=0, ignore_index=False)
            return combined_df
        elif len(dfs) == 1:
            return dfs[0]
        else:
            return dfs
