import pandas as pd
import json
import logging
import subprocess
import tempfile
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_cloc(repo_dir):
    """
    Run cloc on the repository directory and extract line counts from JSON output.
    
    Parameters:
    - repo_dir (str): Path to the cloned repository directory.
    
    Returns:
    - tuple: (blank_lines, code_lines, comment_lines)
    """
    try:
        # Run cloc with --json for structured output
        result = subprocess.check_output(
            ['cloc', repo_dir, '--json', '--exclude-dir=.git'],
            stderr=subprocess.STDOUT
        ).decode('utf-8')
        
        cloc_data = json.loads(result)
        total = cloc_data.get('SUM', {})
        blank_lines = total.get('blank', 0)
        code_lines = total.get('code', 0)
        comment_lines = total.get('comment', 0)
        
        logging.debug(f"cloc results for {repo_dir}: {blank_lines} blank, {code_lines} code, {comment_lines} comment lines")
        return blank_lines, code_lines, comment_lines
    
    except FileNotFoundError:
        logging.error("cloc command not found. Please install cloc (e.g., 'pip install cloc' or 'sudo apt install cloc').")
        return 0, 0, 0
    
    except subprocess.CalledProcessError as e:
        logging.warning(f"cloc failed for {repo_dir}: {e.output.decode() if e.output else str(e)}")
        return 0, 0, 0
    
    except json.JSONDecodeError as e:
        logging.warning(f"Failed to parse cloc JSON output for {repo_dir}: {str(e)}")
        return 0, 0, 0

def count_repo_lines(repo_list, github_token=None, delay=1.0):
    """
    Counts blank, code, and comment lines for each repository by cloning it locally using git
    and running cloc for accurate line counting.
    
    Parameters:
    - repo_list (list of str): List of repositories in 'user_name/repo_name' format.
    - github_token (str, optional): GitHub Personal Access Token for private repos.
    - delay (float, optional): Seconds to sleep between cloning operations (default: 1.0).
    
    Returns:
    - pd.DataFrame: DataFrame with columns ['repository', 'blankLines', 'codeLines', 'commentLines'].
    """
    data = []
    
    for i, repo_str in enumerate(repo_list):
        repo_data = {
            'repository': repo_str,
            'blankLines': 0,
            'codeLines': 0,
            'commentLines': 0
        }
        
        # Construct clone URL
        clone_url = f'https://github.com/{repo_str}.git'
        if github_token:
            clone_url = f'https://oauth2:{github_token}@github.com/{repo_str}.git'
        
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                # Clone the repository (shallow clone for efficiency)
                subprocess.check_call(['git', 'clone', '--depth', '1', clone_url, temp_dir], stderr=subprocess.STDOUT)
                logging.info(f"Successfully cloned {repo_str}")
                
                # Run cloc on the cloned directory
                try:
                    result = subprocess.check_output(['cloc', temp_dir, '--json'], stderr=subprocess.STDOUT).decode('utf-8')
                    cloc_data = json.loads(result)
                    sum_data = cloc_data.get('SUM', {})
                    blank_lines = sum_data.get('blank', 0)
                    code_lines = sum_data.get('code', 0)
                    comment_lines = sum_data.get('comment', 0)
                    
                    repo_data['blankLines'] = blank_lines
                    repo_data['codeLines'] = code_lines
                    repo_data['commentLines'] = comment_lines
                    
                    logging.info(f"Processed {repo_str} with cloc: {blank_lines} blank, {code_lines} code, {comment_lines} comment lines")
                except subprocess.CalledProcessError as e:
                    logging.warning(f"cloc failed for {repo_str}: {e.output.decode('utf-8') if e.output else str(e)}. Using zeros.")
                except json.JSONDecodeError as e:
                    logging.warning(f"Failed to parse cloc JSON for {repo_str}: {str(e)}. Using zeros.")
                except FileNotFoundError:
                    logging.error(f"cloc not found. Please install cloc. Skipping line counts for {repo_str}.")
                
                data.append(repo_data)
                
                # Add delay after cloning, except for the last repository
                if i < len(repo_list) - 1 and delay > 0:
                    logging.debug(f"Sleeping for {delay} seconds before next clone.")
                    time.sleep(delay)
            
            except subprocess.CalledProcessError as e:
                logging.error(f"Failed to clone {repo_str}: {e.output.decode('utf-8') if e.output else str(e)}. Skipping.")
                continue
            
            except Exception as e:
                logging.error(f"Unexpected error for {repo_str}: {str(e)}. Skipping.")
                continue
    
    if not data:
        logging.warning("No data processed for any repositories.")
        return pd.DataFrame()
    
    df = pd.DataFrame(data)
    return df
