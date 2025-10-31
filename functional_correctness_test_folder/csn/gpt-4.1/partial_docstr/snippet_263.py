
import os
import glob
import pandas as pd


class Import_Data:

    def __init__(self):
        ''' Constructor.
        This class stores the imported data.
        '''
        self.data = None

    def import_csv(self, file_name='*', folder_name='.', head_row=0, index_col=0, convert_col=True, concat_files=False):
        if file_name == '*':
            pattern = os.path.join(folder_name, '*.csv')
            files = glob.glob(pattern)
        else:
            if not file_name.lower().endswith('.csv'):
                file_name += '.csv'
            files = [os.path.join(folder_name, file_name)]

        dataframes = []
        for f in files:
            df = self._load_csv(f, folder_name, head_row,
                                index_col, convert_col, concat_files)
            dataframes.append(df)

        if concat_files and len(dataframes) > 0:
            self.data = pd.concat(dataframes, ignore_index=True)
        elif len(dataframes) == 1:
            self.data = dataframes[0]
        else:
            self.data = dataframes

        return self.data

    def _load_csv(self, file_name, folder_name, head_row, index_col, convert_col, concat_files):
        ''' Load single csv file.
        '''
        # file_name is already full path
        df = pd.read_csv(
            file_name,
            header=head_row if head_row is not None else 0
        )
        if index_col > 0:
            df = df.iloc[:, index_col:]
        if convert_col:
            for col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='ignore')
        return df
