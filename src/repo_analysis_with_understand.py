"""
The following Python code will clone repositories one at a time.
Each repo will then be analyzed by Understand. For each analysis report a csv file will be saved.
The reports will be saved in ../data/Understand_analysis_reports folder.
"""
import pandas as pd
import subprocess
import json, os



def analyze_repo(repo_list, data_root_folder = 'data'):
    indexer = 0
    index_dict = {}
    failed_dict = {}
    path_to_data = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', data_root_folder))

    counter = 1
    for repo in repo_list: # change here
        print(f"Processing repo {counter} out of {len(repo_list)}: {repo}")
        counter += 1
        folder_name = repo.replace("/", "_")
        subprocess.run(f"mkdir {path_to_data}/git_repos_for_analysis/{folder_name}", shell=True)
        try:
            subprocess.run(f"git clone https://github.com/{repo}.git {path_to_data}/git_repos_for_analysis/{folder_name}", shell=True)
            subprocess.run(
                f"/Applications/Understand.app/Contents/MacOS/und -db {path_to_data}/git_repos_for_analysis/{folder_name}/{folder_name}.und create -languages Python add {path_to_data}/git_repos_for_analysis/{folder_name} settings -metrics All -metricsShowDeclaredInFile On -metricsDeclaredInFileDisplayMode FullPath -metricsOutputFile {path_to_data}/git_repos_for_analysis/{folder_name}/{folder_name}.csv analyze metrics",
                shell=True)
            
            subprocess.run(
                f"cp {path_to_data}/git_repos_for_analysis/{folder_name}/{folder_name}.csv {path_to_data}/Understand_analysis_reports",
                shell=True)
            subprocess.run(f"rm -rf {path_to_data}/git_repos_for_analysis/{folder_name}", shell=True)
            index_dict[indexer] = (repo, f"{folder_name}.csv")
            indexer += 1
        except Exception as e: # analysis may fail for some project
            subprocess.run(f"rm -rf {path_to_data}/git_repos_for_analysis/{folder_name}", shell=True) # delete the created folder
            failed_dict[repo] = str(e)

    index_df = pd.DataFrame(index_dict).T
    index_df.columns=['repo_name', "expected_analysis_report_file"]

    index_df.to_csv(f"{path_to_data}/metadata_folder/repository_to_file_mapping.csv", index = True)

    # if there were issues running the subprocess commands, log the error messages and the associated repos.
    if len(failed_dict) > 0:
        with open (f"{path_to_data}/metadata_folder/failed_repos.json", 'w') as failed_repos:
            json.dump(failed_dict, failed_repos)
