
import pandas as pd
import os


class Import_Data:
    ''' This class imports data from csv files. '''

    def __init__(self):

        pass

    def import_csv(self, file_name='*', folder_name='.', head_row=0, index_col=0, convert_col=True, concat_files=False):

        self._load_csv(file_name, folder_name, head_row,
                       index_col, convert_col, concat_files)

    def _load_csv(self, file_name, folder_name, head_row, index_col, convert_col, concat_files):

        if file_name == '*':
            file_list = [f for f in os.listdir(
                folder_name) if f.endswith('.csv')]
        else:
            file_list = [file_name]

        data_frames = []
        for file in file_list:
            file_path = os.path.join(folder_name, file)
            df = pd.read_csv(file_path, header=head_row, index_col=index_col)
            if convert_col:
                df = df.apply(pd.to_numeric, errors='ignore')
            data_frames.append(df)

        if concat_files:
            self.data = pd.concat(data_frames, axis=0)
        else:
            self.data = data_frames[0] if len(
                data_frames) == 1 else data_frames
