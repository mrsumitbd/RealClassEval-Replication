from fetch_repo_data import fetch_repo_data
from fetch_code_comment_ratio import count_repo_lines
from class_skeleton_extractor import class_skeleton_extractor
from repo_analysis_with_understand import analyze_repo
import pandas as pd
from utility import refine_indentation
import numpy as np
from datasets import load_dataset
from dotenv import load_dotenv
from github import Auth, Github
import os, sys
load_dotenv('../.env')


def get_csn_repo_list(split_type = None):
    if split_type is not None:
        return load_dataset("code_search_net", 'python',
                        split=split_type, trust_remote_code=True).to_pandas().repository_name.unique()  # returns a list of all unique repos in the dataset.
    else:
        train_repos = load_dataset("code_search_net", 'python',
                        split="train", trust_remote_code=True).to_pandas().repository_name.unique()
        test_repos = load_dataset("code_search_net", 'python',
                        split="test", trust_remote_code=True).to_pandas().repository_name.unique()
        valid_repos = load_dataset("code_search_net", 'python',
                        split="validation", trust_remote_code=True).to_pandas().repository_name.unique()
        return list((set(train_repos).union(set(test_repos))).union(set(valid_repos)))
    
def get_engineered_projects_from_csn(file_path):
    return pd.read_csv(file_path)['repository'].tolist()


if __name__ == "__main__":

    if sys.argv[1] == "pull-csn-repo-data":
        auth = Auth.Token(os.getenv("GH_API_TOKEN"))
        gh_obj = Github(auth=auth)

        repo_list = get_csn_repo_list()
        df = fetch_repo_data(gh_obj, repo_list)
        df.to_csv("../data/repo_data.csv", index=False)

    elif sys.argv[1] == "calculate-code-ratio":
        repos = get_engineered_projects_from_csn("../data/engineered_projects_from_csn.csv")
        df = count_repo_lines(repos)
        df.to_csv("../data/repo_code_comment_ratio_csn_engineered_projects.csv", index=False)
    
    elif sys.argv[1] == "analyze-with-understand":
        repos = get_engineered_projects_from_csn("../data/complete_engineered_csn_projects.csv")
        analyze_repo(repos, data_root_folder='data')
    
    elif sys.argv[1] == "extract-class-skeleton":
        """Main entry point for extracting and saving class skeletons."""
        skeleton_df = class_skeleton_extractor()
        print(skeleton_df.shape)
        
        for col in skeleton_df.columns:
            if skeleton_df[col].dtype == object:
                skeleton_df[col] = skeleton_df[col].apply(
                    lambda x: np.nan if x == np.nan else str(x).encode('utf-8', 'replace').decode('utf-8'))
        skeleton_df['code_skeleton'] = [refine_indentation(skeleton) for skeleton in skeleton_df['code_skeleton'].tolist()]
        skeleton_df.to_csv("../data/metadata_folder/extracted_class_skeletons-raw_version.csv", index=False)
    else:
        raise ValueError("Invalid argument. Use 'pull-csn-repo-data' or 'calculate-code-ratio' or 'extract-class-skeleton'.")
