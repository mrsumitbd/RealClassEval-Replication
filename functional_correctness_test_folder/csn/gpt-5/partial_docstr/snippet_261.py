import os
import glob
from typing import Union, Dict, List
import pandas as pd


class Import_Data:
    ''' This class imports data from csv files. '''

    def __init__(self):
        self.last_files: List[str] = []
        self.last_result = None

    def import_csv(self, file_name='*', folder_name='.', head_row=0, index_col=0, convert_col=True, concat_files=False):
        files = self._resolve_files(file_name, folder_name)
        if not files:
            raise FileNotFoundError(
                f'No CSV files found for pattern "{file_name}" in "{folder_name}".')
        results: Dict[str, pd.DataFrame] = {}
        for f in files:
            df = self._load_csv(f, folder_name, head_row,
                                index_col, convert_col, concat_files)
            results[os.path.basename(f)] = df

        self.last_files = files

        if concat_files:
            concatenated = pd.concat(
                [results[k].assign(_source_file=k) for k in results],
                axis=0,
                ignore_index=False
            )
            self.last_result = concatenated
            return concatenated

        if len(results) == 1:
            single = next(iter(results.values()))
            self.last_result = single
            return single

        self.last_result = results
        return results

    def _load_csv(self, file_name, folder_name, head_row, index_col, convert_col, concat_files):
        path = file_name if os.path.isabs(
            file_name) else os.path.join(folder_name, file_name)
        if not os.path.exists(path):
            raise FileNotFoundError(f'File not found: {path}')

        df = pd.read_csv(path, header=head_row if head_row is not None else 'infer',
                         index_col=index_col if index_col is not None else None)

        if convert_col:
            for col in df.columns:
                try:
                    df[col] = pd.to_numeric(df[col], errors='ignore')
                except Exception:
                    pass
        return df

    def _resolve_files(self, file_name: Union[str, List[str]], folder_name: str) -> List[str]:
        if isinstance(file_name, list):
            files = []
            for f in file_name:
                pattern = f if os.path.isabs(
                    f) else os.path.join(folder_name, f)
                if any(ch in f for ch in ['*', '?', '[']):
                    files.extend(sorted(glob.glob(pattern)))
                else:
                    path = pattern
                    if path.lower().endswith('.csv') and os.path.exists(path):
                        files.append(path)
                    else:
                        candidate = path if path.lower().endswith(
                            '.csv') else f'{path}.csv'
                        if os.path.exists(candidate):
                            files.append(candidate)
            return sorted(set(files))

        pattern = file_name
        if not any(ch in pattern for ch in ['*', '?', '[']):
            base = file_name if os.path.isabs(
                file_name) else os.path.join(folder_name, file_name)
            if base.lower().endswith('.csv'):
                return [base] if os.path.exists(base) else []
            candidate = f'{base}.csv'
            return [candidate] if os.path.exists(candidate) else []

        search_pattern = pattern if os.path.isabs(pattern) else os.path.join(
            folder_name, pattern if pattern.endswith('.csv') else f'{pattern}.csv' if pattern != '*' else '*.csv')
        return sorted(glob.glob(search_pattern))
