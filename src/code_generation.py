import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
from generation_with_openai import batch_generate_with_openai, batch_few_shot_generation_with_openai
from generation_with_togetherai import generate_with_together, few_shot_generation_with_together
from generation_with_mistral import generate_with_mistral, few_shot_generation_with_mistral
from utility import list_files
import sys, os

path_to_data = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'data'))

def prepare_for_code_generation(docstr_df_path, test_suite_path):
    df = pd.read_csv(docstr_df_path)

    test_files = list_files(test_suite_path, all_files=False, extension='py')

    snippets_with_test_suites = [f.split(".py")[0].split("test_")[1] for f in test_files]

    test_suite_present = []
    for _, row in df.iterrows():
        if row['snippet_id'] in snippets_with_test_suites:
            test_suite_present.append(True)
        else:
            test_suite_present.append(False)
    
    df['test_suite_present'] = test_suite_present
    df_filtered = df[df['test_suite_present'] == True]

    return df_filtered[['id', 'repository_name', 'file_path', 'class_name',
       'human_written_code', 'class_skeleton', 'snippet_id']]

def load_baseline():
    return pd.read_csv(f"{path_to_data}/functional_correctness_data/ClassEval/dfs/full_docstr.csv")

if __name__ == "__main__":
    data_version = sys.argv[1]  # e.g., 'csn'
    api_provider = sys.argv[2]  # 'openai' or 'together'
    docstr_type = sys.argv[3]  # e.g., 'full_docstr' or 'partial_docstr'
    model = sys.argv[4]  # e.g., 'gpt-4o', 'gpt-3.5-turbo', 'together-guanaco-70b'
    ablation_study = sys.argv[5] # Yes or No
    rag = sys.argv[6] # Yes or No

    if ablation_study == 'No':
        if data_version != 'ClassEval':
            prepared_df = prepare_for_code_generation(docstr_df_path=f"{path_to_data}/functional_correctness_data/{data_version}/dfs/{docstr_type}.csv",
                                                      test_suite_path=f"{path_to_data}/functional_correctness_data/{data_version}/pynguin_generated_tests/full_docstr")
            prepared_df.dropna(subset=['class_skeleton'], inplace=True)
        else:
            prepared_df = load_baseline()
        skeletons = prepared_df['class_skeleton'].tolist()
        snippet_list = prepared_df['snippet_id'].tolist()
        print(f"Total skeletons available for code generation: {len(skeletons)}")

    else:
        prepared_df = pd.read_csv(f"{path_to_data}/functional_correctness_data/{data_version}/dfs/{docstr_type}.csv")
        skeletons = prepared_df['class_skeleton'].tolist()
        snippet_list = prepared_df['snippet_id'].tolist()
        print(f"Total skeletons available for code generation: {len(skeletons)}")

    if api_provider == 'together':
        if rag.lower() == 'no':
            generated = generate_with_together(skeletons, model=model)
            prepared_df[f'{model}_generated_code'] = generated
            prepared_df.dropna(inplace=True)
            prepared_df.to_csv(f"{path_to_data}/generated_code/{data_version}/{docstr_type}/{model.split('/')[0]}.csv", index=False)
        else:
            generated = few_shot_generation_with_together(snippet_ids=snippet_list, model=model,prompt_location="../rag_experiments/output/prompts")
            prepared_df[f'{model}_generated_code'] = generated
            prepared_df.dropna(inplace=True)
            prepared_df.to_csv(f"{path_to_data}/generated_code/{data_version}/{docstr_type}/{rag}_{model.split('/')[0]}.csv", index=False)

    elif api_provider == 'openai':
        if rag.lower() == 'no':
            generated = batch_generate_with_openai(skeletons, model, reasoning_effort='low')  # Or 'low'/'high'
            prepared_df[f'{model}_generated_code'] = generated
            prepared_df.dropna(inplace=True)
            prepared_df.to_csv(f"{path_to_data}/generated_code/{data_version}/{docstr_type}/{model}.csv", index=False)
        else:
            generated = batch_few_shot_generation_with_openai(snippet_ids=snippet_list, model=model, prompt_location="../rag_experiments/output/prompts")
            prepared_df[f'{model}_generated_code'] = generated
            prepared_df.dropna(inplace=True)
            prepared_df.to_csv(f"{path_to_data}/generated_code/{data_version}/{docstr_type}/{rag}_{model}.csv", index=False)

    elif api_provider == 'mistral':
        if rag.lower() == 'no':
            generated = generate_with_mistral(skeletons, model)
            prepared_df[f'{model}_generated_code'] = generated
            prepared_df.dropna(inplace=True)
            prepared_df.to_csv(f"{path_to_data}/generated_code/{data_version}/{docstr_type}/{model.split('-')[0]}.csv", index=False)
        else:
            generated = few_shot_generation_with_mistral(snippet_ids=snippet_list, model=model,
                                                          prompt_location="../rag_experiments/output/prompts")
            prepared_df[f'{model}_generated_code'] = generated
            prepared_df.dropna(inplace=True)
            prepared_df.to_csv(
                f"{path_to_data}/generated_code/{data_version}/{docstr_type}/{rag}_{model.split('-')[0]}.csv",
                index=False)
