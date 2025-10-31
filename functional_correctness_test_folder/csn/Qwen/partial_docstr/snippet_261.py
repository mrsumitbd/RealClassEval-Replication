
import os
import pandas as pd


class Import_Data:
    ''' This class imports data from csv files. '''

    def __init__(self):
        pass

    def import_csv(self, file_name='*', folder_name='.', head_row=0, index_col=0, convert_col=True, concat_files=False):
        if file_name == '*':
            files = [f for f in os.listdir(folder_name) if f.endswith('.csv')]
        else:
            files = [file_name]

        dataframes = []
        for file in files:
            df = self._load_csv(file, folder_name, head_row,
                                index_col, convert_col, concat_files)
            dataframes.append(df)

        if concat_files and len(dataframes) > 1:
            return pd.concat(dataframes, ignore_index=True)
        elif len(dataframes) == 1:
            return dataframes[0]
        else:
            return dataframes

    def _load_csv(self, file_name, folder_name, head_row, index_col, convert_col, concat_files):
        file_path = os.path.join(folder_name, file_name)
        df = pd.read_csv(file_path, header=head_row, index_col=index_col)
        if convert_col:
            for col in df.select_dtypes(include=['object']).columns:
                df[col] = pd.to_numeric(df[col], errors='ignore')
        return df
