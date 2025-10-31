import pandas as pd
from rag_dataframe_converter import convert_dataframe_to_dataset, convert_v2_dataframe_to_dataset
import sys

df = pd.read_csv(sys.argv[1])
if sys.argv[1].split("/dfs")[0].split("_data/")[1] == 'csn':
    convert_dataframe_to_dataset(
        df.sample(n = 5000, random_state=42).reset_index(drop=True),
        output_path=f'../../rag_experiments/{sys.argv[1].split("/dfs")[0].split("_data/")[1]}.json',
        include_metadata=False  # or True if you want metrics
    )
else:
    stats = convert_v2_dataframe_to_dataset(
        df,
        output_path=f'../../rag_experiments/{sys.argv[1].split("/dfs")[0].split("_data/")[1]}.json',
    )

    print(f"Has snippet_id: {stats['has_snippet_id']}")
