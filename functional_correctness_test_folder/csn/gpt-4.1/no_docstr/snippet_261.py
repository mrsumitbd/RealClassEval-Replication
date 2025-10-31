
import os
import glob
import pandas as pd


class Import_Data:

    def __init__(self):
        pass

    def import_csv(self, file_name='*', folder_name='.', head_row=0, index_col=0, convert_col=True, concat_files=False):
        return self._load_csv(file_name, folder_name, head_row, index_col, convert_col, concat_files)

    def _load_csv(self, file_name, folder_name, head_row, index_col, convert_col, concat_files):
        # Build file pattern
        if file_name == '*':
            pattern = os.path.join(folder_name, '*.csv')
        else:
            if not file_name.endswith('.csv'):
                file_name += '.csv'
            pattern = os.path.join(folder_name, file_name)
        file_list = sorted(glob.glob(pattern))
        if not file_list:
            raise FileNotFoundError(
                f"No CSV files found for pattern: {pattern}")

        dfs = []
        for f in file_list:
            df = pd.read_csv(f, header=head_row, index_col=index_col)
            if convert_col:
                for col in df.columns:
                    try:
                        df[col] = pd.to_numeric(df[col])
                    except Exception:
                        pass
            dfs.append(df)

        if concat_files:
            result = pd.concat(dfs, axis=0)
            return result
        else:
            if len(dfs) == 1:
                return dfs[0]
            else:
                return dfs
