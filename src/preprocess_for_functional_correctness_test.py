import sys, autopep8, subprocess
import pandas as pd

def extract_code_from_llm_response(response):
    try:
        if "```python" in response:
            return autopep8.fix_code(response.split("```python")[1].split("```")[0])
        else:
            return autopep8.fix_code(response)
    except:
        return None

def copy_required_files(df):
    for _, row in df.iterrows():
        if sys.argv[4].lower() == "no":
            f = open(f'../functional_correctness_test_folder/{sys.argv[1]}/{sys.argv[2]}/{sys.argv[3]}/{row["snippet_id"]}.py', 'w')
        else:
            f = open(
                f'../functional_correctness_test_folder/{sys.argv[1]}/rag/{sys.argv[2]}/{sys.argv[3]}/{row["snippet_id"]}.py',
                'w')
        f.write(row['relevant_code'])
        f.close()
        if sys.argv[1] != 'ClassEval':
            if sys.argv[4].lower() == "no":
                cp_cmd = f'cp ../data/functional_correctness_data/{sys.argv[1]}/pynguin_generated_tests/full_docstr/test_{row["snippet_id"]}.py ../functional_correctness_test_folder/{sys.argv[1]}/{sys.argv[2]}/{sys.argv[3]}/'
            else:
                cp_cmd = f'cp ../data/functional_correctness_data/{sys.argv[1]}/pynguin_generated_tests/full_docstr/test_{row["snippet_id"]}.py ../functional_correctness_test_folder/{sys.argv[1]}/rag/{sys.argv[2]}/{sys.argv[3]}/'
        else:
            cp_cmd = f'cp ../data/functional_correctness_data/{sys.argv[1]}/test_suits/full_docstr/test_{row["snippet_id"]}.py ../functional_correctness_test_folder/{sys.argv[1]}/{sys.argv[2]}/{sys.argv[3]}/'
        subprocess.run(cp_cmd, shell=True)




if __name__ == "__main__":

    """
    sys.argv[1] -> csn / post_cut-off
    sys.argv[2] -> Qwen / codestral etc
    sys.argv[3] -> full_docstr, no_docstr etc
    sys.argv[4] -> rag  # Yes or NO
    """

    if sys.argv[4].lower() == 'no':
        generated_code_df = pd.read_csv(f"../data/generated_code/{sys.argv[1]}/{sys.argv[3]}/{sys.argv[2]}.csv")
    else:
        generated_code_df = pd.read_csv(f"../data/generated_code/{sys.argv[1]}/{sys.argv[3]}/rag/{sys.argv[2]}.csv")

    print(generated_code_df.shape)

    cols = [col if "generated_code" not in col else "generated_code" for col in generated_code_df.columns]
    generated_code_df.columns = cols

    generated_code_df['relevant_code'] = [extract_code_from_llm_response(code) for code in generated_code_df['generated_code']]

    generated_code_df.dropna(subset=["relevant_code"], inplace=True)

    print(generated_code_df.shape)

    if sys.argv[4].lower() == 'no':
        mkdir_cmd1 = f"mkdir -p ../functional_correctness_test_folder/{sys.argv[1]}/{sys.argv[2]}/{sys.argv[3]}/"
        mkdir_cmd2 = f"mkdir -p ../functional_correctness_test_folder/{sys.argv[1]}/{sys.argv[2]}/{sys.argv[3]}_reports/per_snippet/"
    else:
        mkdir_cmd1 = f"mkdir -p ../functional_correctness_test_folder/{sys.argv[1]}/rag/{sys.argv[2]}/{sys.argv[3]}/"
        mkdir_cmd2 = f"mkdir -p ../functional_correctness_test_folder/{sys.argv[1]}/rag/{sys.argv[2]}/{sys.argv[3]}_reports/per_snippet/"

    subprocess.run(mkdir_cmd1, shell=True)
    subprocess.run(mkdir_cmd2, shell=True)

    copy_required_files(generated_code_df)
