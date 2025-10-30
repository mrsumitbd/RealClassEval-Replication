from concurrent.futures import ProcessPoolExecutor, as_completed
import os
import sys
import subprocess
import pandas as pd
from utility import list_files

def run_single_test(test_file):
    """Run a single test file with timeout"""
    print(f"Running tests in {test_file}")
    try:
        if sys.argv[4].lower() == 'no':
            subprocess.run([sys.executable, '-m', 'pytest',
                                         "--continue-on-collection-errors",
                                         "-q",
                                         "--csv",
                                         f"../functional_correctness_test_folder/{sys.argv[1]}/{sys.argv[2]}/{sys.argv[3]}_reports/per_snippet/test_results_{test_file.split('test_')[1].split('.py')[0]}.csv",
                                         f'../functional_correctness_test_folder/{sys.argv[1]}/{sys.argv[2]}/{sys.argv[3]}/{test_file}'],
                                        capture_output=True, text=True, timeout=30)
        else:
            subprocess.run([sys.executable, '-m', 'pytest',
                            "--continue-on-collection-errors",
                            "-q",
                            "--csv",
                            f"../functional_correctness_test_folder/{sys.argv[1]}/rag/{sys.argv[2]}/{sys.argv[3]}_reports/per_snippet/test_results_{test_file.split('test_')[1].split('.py')[0]}.csv",
                            f'../functional_correctness_test_folder/{sys.argv[1]}/rag/{sys.argv[2]}/{sys.argv[3]}/{test_file}'],
                           capture_output=True, text=True, timeout=30)
        print(f"Finished tests in {test_file}")
        return test_file, "success"
    except subprocess.TimeoutExpired:
        print(f"Test {test_file} timed out after 30 seconds. Skipping and deleting files.")

        # Delete the test file
        if sys.argv[4].lower() == 'no':
            test_file_path = f'../functional_correctness_test_folder/{sys.argv[1]}/{sys.argv[2]}/{sys.argv[3]}/{test_file}'
        else:
            test_file_path = f'../functional_correctness_test_folder/{sys.argv[1]}/rag/{sys.argv[2]}/{sys.argv[3]}/{test_file}'
        if os.path.exists(test_file_path):
            os.remove(test_file_path)
            print(f"Deleted test file: {test_file_path}")

        # Delete the corresponding code file (remove 'test_' prefix from filename)
        code_file = test_file.replace('test_', '')
        if sys.argv[4].lower() == 'no':
            code_file_path = f'../functional_correctness_test_folder/{sys.argv[1]}/{sys.argv[2]}/{sys.argv[3]}/{code_file}'
        else:
            code_file_path = f'../functional_correctness_test_folder/{sys.argv[1]}/rag/{sys.argv[2]}/{sys.argv[3]}/{code_file}'
        if os.path.exists(code_file_path):
            os.remove(code_file_path)
            print(f"Deleted code file: {code_file_path}")
        
        return test_file, "timeout"

def run_tests(test_files, max_workers=4):
    """Run tests in parallel"""
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(run_single_test, test_file): test_file 
                   for test_file in test_files}
        
        for future in as_completed(futures):
            test_file = futures[future]
            try:
                result = future.result()
            except Exception as e:
                print(f"Test {test_file} generated an exception: {e}")
    
    print("All tests completed.")

def combine_tests():
    # Combine all CSV files into a single DataFrame
    if sys.argv[4].lower() == 'no':
        reports = list_files(folder_path=f'../functional_correctness_test_folder/{sys.argv[1]}/{sys.argv[2]}/{sys.argv[3]}_reports/per_snippet/',
                         all_files=False, extension='csv')
    else:
        reports = list_files(
            folder_path=f'../functional_correctness_test_folder/{sys.argv[1]}/rag/{sys.argv[2]}/{sys.argv[3]}_reports/per_snippet/',
            all_files=False, extension='csv')
    all_reports_df = pd.DataFrame()
    for report in reports:
        try:
            if sys.argv[4].lower() == 'no':
                report_df = pd.read_csv(f'../functional_correctness_test_folder/{sys.argv[1]}/{sys.argv[2]}/{sys.argv[3]}_reports/per_snippet/{report}')
            else:
                report_df = pd.read_csv(
                    f'../functional_correctness_test_folder/{sys.argv[1]}/rag/{sys.argv[2]}/{sys.argv[3]}_reports/per_snippet/{report}')
            all_reports_df = pd.concat([all_reports_df, report_df], axis=0)
        except FileNotFoundError:
            print(f"Couldn't find report {report}")

    if sys.argv[4].lower() == 'no':
        all_reports_df.to_csv(f'../functional_correctness_test_folder/{sys.argv[1]}/{sys.argv[2]}/{sys.argv[3]}_reports/combined_test_report.csv',
                          index=False)
    else:
        all_reports_df.to_csv(
            f'../functional_correctness_test_folder/{sys.argv[1]}/rag/{sys.argv[2]}/{sys.argv[3]}_reports/combined_test_report.csv',
            index=False)
    print(f"Combined report saved.")

if __name__ == "__main__":

    """
    sys.argv[1] -> csn / post_cut-off
    sys.argv[2] -> Qwen / codestral etc
    sys.argv[3] -> full_docstr, no_docstr etc
    sys.argv[4] -> rag # Yes or No
    """
    if sys.argv[4].lower() == 'no':
        run_tests([f for f in list_files(f"../functional_correctness_test_folder/{sys.argv[1]}/{sys.argv[2]}/{sys.argv[3]}/", extension="py") if
                   "test_" in f])
    else:
        run_tests([f for f in
                   list_files(f"../functional_correctness_test_folder/{sys.argv[1]}/rag/{sys.argv[2]}/{sys.argv[3]}/",
                              extension="py") if
                   "test_" in f])

    combine_tests()
