import os
from pathlib import Path
from typing import Union, List, Dict
import pandas as pd
import glob


class Import_Data:

    def __init__(self):
        self.last_data = None
        self.last_files: List[Path] = []

    def import_csv(self, file_name='*', folder_name='.', head_row=0, index_col=0, convert_col=True, concat_files=False):
        return self._load_csv(
            file_name=file_name,
            folder_name=folder_name,
            head_row=head_row,
            index_col=index_col,
            convert_col=convert_col,
            concat_files=concat_files
        )

    def _load_csv(self, file_name: Union[str, List[Union[str, Path]]], folder_name: Union[str, Path], head_row, index_col, convert_col: bool, concat_files: bool):
        folder = Path(folder_name).expanduser().resolve()

        def normalize_pattern(name: str) -> str:
            if any(ch in name for ch in ["*", "?", "["]):
                return name
            # If direct file path provided
            p = Path(name)
            if p.suffix:  # has extension
                return str(p)
            # otherwise assume csv extension
            return f"{name}.csv"

        files: List[Path] = []

        if isinstance(file_name, (list, tuple)):
            for fn in file_name:
                f = Path(fn)
                if f.exists():
                    files.append(f.resolve())
                else:
                    pattern = normalize_pattern(str(fn))
                    matches = [Path(m).resolve()
                               for m in glob.glob(str(folder / pattern))]
                    files.extend(matches)
        else:
            # single name or pattern
            pattern = normalize_pattern(str(file_name))
            # If it's an absolute path to a file
            p = Path(pattern)
            if p.exists() and p.is_file():
                files = [p.resolve()]
            else:
                files = [Path(m).resolve()
                         for m in glob.glob(str(folder / pattern))]

        # Filter for csv-like files if no explicit extension given
        if isinstance(file_name, str) and not Path(file_name).suffix and not any(ch in file_name for ch in ["*", "?", "["]):
            files = [f for f in files if f.suffix.lower() == ".csv"]

        # Final fallback: if user gave '*' default, ensure csv only
        if file_name == '*' or (isinstance(file_name, str) and '*' in file_name and '.csv' not in file_name.lower()):
            files = [f for f in files if f.suffix.lower() == ".csv"]

        # Deduplicate and sort
        files = sorted(set(files))

        if not files:
            raise FileNotFoundError(
                "No CSV files matched the given name/pattern and folder.")

        def read_one(path: Path) -> pd.DataFrame:
            df = pd.read_csv(
                path,
                header=head_row,
                index_col=index_col if index_col is not None else None
            )
            if convert_col:
                # Try numeric conversion on object columns
                for col in df.columns:
                    if pd.api.types.is_object_dtype(df[col]):
                        converted_num = pd.to_numeric(df[col], errors='ignore')
                        df[col] = converted_num
                # Optional: convert dtypes to best possible
                df = df.convert_dtypes()
            return df

        dataframes: Dict[Path, pd.DataFrame] = {}
        for f in files:
            dataframes[f] = read_one(f)

        self.last_files = files

        if concat_files:
            result = pd.concat(
                list(dataframes.values()),
                axis=0,
                ignore_index=False,
                sort=False
            )
            self.last_data = result
            return result

        if len(files) == 1:
            self.last_data = dataframes[files[0]]
            return dataframes[files[0]]

        # Multiple files: return dict keyed by file name
        result_dict = {f.name: df for f, df in dataframes.items()}
        self.last_data = result_dict
        return result_dict
