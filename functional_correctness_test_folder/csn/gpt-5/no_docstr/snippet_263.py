import os
import glob
import pandas as pd


class Import_Data:
    def __init__(self):
        pass

    def import_csv(self, file_name='*', folder_name='.', head_row=0, index_col=0, convert_col=True, concat_files=False):
        paths = self._resolve_paths(file_name, folder_name)
        if not paths:
            raise FileNotFoundError(
                f"No CSV files matched for file_name={file_name!r} in folder_name={folder_name!r}")

        dataframes = {}
        for p in paths:
            df = self._load_csv(p, folder_name, head_row,
                                index_col, convert_col, concat_files)
            dataframes[os.path.basename(p)] = df

        if concat_files:
            if not dataframes:
                return pd.DataFrame()
            return pd.concat(list(dataframes.values()), axis=0, ignore_index=False, sort=False)

        if len(dataframes) == 1:
            return next(iter(dataframes.values()))
        return dataframes

    def _load_csv(self, file_name, folder_name, head_row, index_col, convert_col, concat_files):
        path = file_name if os.path.isabs(
            file_name) else os.path.join(folder_name, file_name)

        header = head_row if head_row is not None else None
        idx_col = index_col if index_col is not None else None

        try:
            df = pd.read_csv(path, header=header, index_col=idx_col)
        except UnicodeDecodeError:
            df = pd.read_csv(path, header=header,
                             index_col=idx_col, encoding='latin-1')

        if convert_col:
            # Strip whitespace from string columns
            obj_cols = df.select_dtypes(include=['object']).columns
            for col in obj_cols:
                df[col] = df[col].map(lambda x: x.strip()
                                      if isinstance(x, str) else x)

            # Try to convert to numeric where possible
            for col in df.columns:
                if pd.api.types.is_object_dtype(df[col]):
                    converted = pd.to_numeric(df[col], errors='ignore')
                    df[col] = converted

        return df

    def _resolve_paths(self, file_name, folder_name):
        if isinstance(file_name, (list, tuple)):
            paths = []
            for f in file_name:
                if any(ch in str(f) for ch in ['*', '?', '[']):
                    pattern = f
                    if not os.path.isabs(pattern):
                        pattern = os.path.join(folder_name, pattern if pattern.endswith(
                            '.csv') or '.' in os.path.basename(pattern) else pattern + '.csv')
                    paths.extend(glob.glob(pattern))
                else:
                    p = f if os.path.isabs(f) else os.path.join(folder_name, f)
                    if os.path.isdir(p):
                        p = os.path.join(p, '*.csv')
                        paths.extend(glob.glob(p))
                    else:
                        if not os.path.splitext(p)[1]:
                            p = p + '.csv'
                        if os.path.exists(p):
                            paths.append(p)
            return sorted(set(paths))

        # Single string case
        if file_name in (None, '', '*'):
            pattern = os.path.join(folder_name, '*.csv')
            return sorted(glob.glob(pattern))

        if any(ch in str(file_name) for ch in ['*', '?', '[']):
            pattern = file_name if os.path.isabs(
                file_name) else os.path.join(folder_name, file_name)
            if not os.path.splitext(pattern)[1] or pattern.endswith('.*'):
                # Ensure it targets csv if no extension specified
                if pattern.endswith('.*'):
                    pattern = pattern[:-2] + 'csv'
                elif not pattern.lower().endswith('.csv'):
                    if pattern.endswith('*'):
                        pattern = pattern + '.csv'
            return sorted(glob.glob(pattern))

        # Plain file name
        p = file_name if os.path.isabs(
            file_name) else os.path.join(folder_name, file_name)
        if not os.path.splitext(p)[1]:
            p = p + '.csv'
        return [p] if os.path.exists(p) else []
