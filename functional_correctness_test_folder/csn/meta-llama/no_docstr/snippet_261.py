
import pandas as pd
import glob
import os


class Import_Data:

    def __init__(self):
        self.data = None

    def import_csv(self, file_name='*', folder_name='.', head_row=0, index_col=0, convert_col=True, concat_files=False):
        self.data = self._load_csv(
            file_name, folder_name, head_row, index_col, convert_col, concat_files)
        return self.data

    def _load_csv(self, file_name, folder_name, head_row, index_col, convert_col, concat_files):
        file_path = os.path.join(folder_name, file_name)
        files = glob.glob(file_path)

        if not files:
            raise FileNotFoundError(f"No files found matching {file_path}")

        dataframes = []
        for file in files:
            try:
                df = pd.read_csv(file, header=head_row, index_col=index_col)
                if convert_col:
                    df = df.apply(pd.to_numeric, errors='ignore')
                dataframes.append(df)
            except Exception as e:
                print(f"Error loading {file}: {str(e)}")

        if concat_files:
            if dataframes:
                return pd.concat(dataframes, ignore_index=True)
            else:
                return None
        else:
            if len(dataframes) == 1:
                return dataframes[0]
            else:
                return dataframes
