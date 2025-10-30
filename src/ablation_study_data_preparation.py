import sys
import pandas as pd
import re
from utility import refine_indentation, remove_multiline_comments
from code_generation import prepare_for_code_generation
import numpy as np

def ablation_data_prep(df, keep_docstr):
    full_docstr_df = pd.read_csv(f'../data/functional_correctness_data/{sys.argv[1]}/dfs/full_docstr.csv')
    prepared_df = df.copy(deep = True)
    prepared_df = pd.merge(left=prepared_df, right=full_docstr_df[['id', 'total_program_units']], on='id', how='inner')
    prepared_df.dropna(subset=['class_skeleton'], inplace=True)
    modified_skeleton_list = []
    modified_total_docstr = []
    random_num_generator = np.random.default_rng(54321)
    if keep_docstr == 'partial':
        for idx, row in prepared_df.iterrows():
            total_units = row['total_program_units']
            unit_list = row['class_skeleton'].split("def")
            idx_list = random_num_generator.choice(list(range(1, total_units + 1)), size = random_num_generator.integers(low = 1, high = total_units, size = 1), replace=False,)
            idx_list.sort()
            modified_total_docstr.append(total_units - len(idx_list))

            ablation_list = []
            i = 1
            for unit in unit_list:
                if i in idx_list:
                    edited_unit = remove_multiline_comments(unit_list[i-1])
                    ablation_list.append(edited_unit)
                else:
                    ablation_list.append(unit)
                i += 1
            modified_skeleton_list.append("def".join(ablation_list))
    else:
        for idx, row in prepared_df.iterrows():
            modified_total_docstr.append(0)
            modified_skeleton_list.append(re.sub(r"\n{1,}", "\n", remove_multiline_comments(row['class_skeleton']), re.MULTILINE).replace("pass", "pass\n"))

    prepared_df['class_skeleton'] = [refine_indentation(skeleton) for skeleton in modified_skeleton_list]
    return prepared_df


if __name__ == "__main__":
    tmp_df = prepare_for_code_generation(docstr_df_path =
                                         f'../data/functional_correctness_data/{sys.argv[1]}/dfs/full_docstr.csv',
                                         test_suite_path = f'../data/functional_correctness_data/{sys.argv[1]}/pynguin_generated_tests/full_docstr')

    ab_partial_docstr_df = ablation_data_prep(tmp_df, keep_docstr='partial')

    ab_partial_docstr_df.to_csv(f'../data/functional_correctness_data/{sys.argv[1]}/dfs/partial_docstr.csv', index=False)

    ab_no_docstr_df = ablation_data_prep(tmp_df, keep_docstr='no')

    ab_no_docstr_df.to_csv(f'../data/functional_correctness_data/{sys.argv[1]}/dfs/no_docstr.csv', index=False)
