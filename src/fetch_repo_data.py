import pandas as pd
from github import Github, GithubException, UnknownObjectException, RateLimitExceededException
import time
import json
import logging
from functools import wraps
import requests.exceptions
from datetime import datetime, timezone

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def handle_rate_limit(max_retries=3, base_delay=60):
    """
    Decorator to handle GitHub API rate limits with exponential backoff.
    
    Args:
        max_retries (int): Maximum number of retry attempts
        base_delay (int): Base delay in seconds before retrying
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            
            while retries <= max_retries:
                try:
                    return func(*args, **kwargs)
                    
                except RateLimitExceededException as e:
                    if retries == max_retries:
                        logger.error(f"Max retries ({max_retries}) exceeded for rate limit")
                        raise e
                    
                    # Get rate limit info
                    github_instance = None
                    for arg in args:
                        if isinstance(arg, Github):
                            github_instance = arg
                            break
                    
                    if github_instance:
                        rate_limit = github_instance.get_rate_limit()
                        reset_time = rate_limit.core.reset
                        wait_time = (reset_time - datetime.now(timezone.utc)).total_seconds() + 10  # Add 10s buffer
                    else:
                        wait_time = base_delay * (2 ** retries)  # Exponential backoff
                    
                    wait_time = max(wait_time, 0)  # Ensure non-negative
                    logger.warning(f"Rate limit exceeded. Waiting {wait_time:.0f} seconds before retry {retries + 1}/{max_retries}")
                    time.sleep(wait_time)
                    retries += 1
                    
                except (requests.exceptions.RequestException, GithubException) as e:
                    if retries == max_retries:
                        logger.error(f"Max retries ({max_retries}) exceeded for network/API error: {e}")
                        raise e
                    
                    wait_time = base_delay * (2 ** retries)
                    logger.warning(f"Network/API error: {e}. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    retries += 1
                    
            return None
        return wrapper
    return decorator

@handle_rate_limit(max_retries=5, base_delay=60)
def fetch_repo_data(g, repo_list):
    """
    Fetches GitHub repository data using PyGitHub and returns a pandas DataFrame.
    
    Parameters:
    - g (obj): Authenticated (Py)Github object.
    - repo_list (list of str): List of repositories in 'user_name/repo_name' format.
    
    Returns:
    - pd.DataFrame: DataFrame with each row representing a repository and columns for the fetched data.
    """
    
    data = []
    
    for repo_str in repo_list:
        try:
            logging.info(f"Processing repository: {repo_str}")
                
            owner, repo_name = repo_str.split('/')
            repo = g.get_repo(f"{owner}/{repo_name}")
            
            # Fetch last commit info safely
            last_commit_message = None
            last_commit_sha = None
            commits = repo.get_commits()
            if commits.totalCount > 0:
                latest_commit = commits[0]
                last_commit_message = latest_commit.commit.message
                last_commit_sha = latest_commit.sha
            
            # Fetch data
            repo_data = {
                'repository': repo_str,
                'isFork': repo.fork,
                'commits': commits.totalCount,
                'branches': repo.get_branches().totalCount,
                'releases': repo.get_releases().totalCount,
                'forks': repo.forks_count,
                'mainLanguage': repo.language,
                'defaultBranch': repo.default_branch,
                'license': repo.license.name if repo.license else None,
                'homepage': repo.homepage,
                'watchers': repo.subscribers_count,
                'stargazers': repo.stargazers_count,
                'contributors': repo.get_contributors().totalCount,
                'size': repo.size,
                'createdAt': repo.created_at,
                'pushedAt': repo.pushed_at,
                'updatedAt': repo.updated_at,
                'totalIssues': repo.get_issues(state='all').totalCount,
                'openIssues': repo.open_issues_count,
                'totalPullRequests': repo.get_pulls(state='all').totalCount,
                'openPullRequests': repo.get_pulls(state='open').totalCount,
                'lastCommit': last_commit_message,
                'lastCommitSHA': last_commit_sha,
                'hasWiki': repo.has_wiki,
                'isArchived': repo.archived,
                'isDisabled': repo.disabled,
                'languages': json.dumps(repo.get_languages()),  # Store as JSON string
                'labels': json.dumps([label.name for label in repo.get_labels()]),  # Store as JSON string
                'topics': json.dumps(repo.get_topics())  # Store as JSON string
            }
            
            data.append(repo_data)
            logging.info(f"Successfully fetched data for {repo_str}")
        
        except UnknownObjectException:
            logging.error(f"Repository {repo_str} not found or inaccessible. Skipping.")
            continue
        
        except RateLimitExceededException:
            try:
                reset_time = g.get_rate_limit().get('resources', {}).get('core', {}).get('reset', time.time() + 3600)
                sleep_time = reset_time - time.time() + 60  # Add 1-minute buffer
                logging.info(f"Rate limit exceeded for {repo_str}. Sleeping until {time.ctime(reset_time)} (approx {sleep_time:.0f} seconds).")
                time.sleep(max(sleep_time, 0))
                continue  # Retry the current repo after sleep
            except Exception as e:
                logging.warning(f"Failed to get rate limit reset time for {repo_str}: {str(e)}. Skipping.")
                continue
        
        except GithubException as e:
            logging.error(f"GitHub API error for {repo_str}: {str(e)}. Skipping.")
            continue
        
        except Exception as e:
            logging.error(f"Unexpected error for {repo_str}: {str(e)}. Skipping.")
            continue
    
    if not data:
        logging.warning("No data fetched for any repositories.")
        return pd.DataFrame()
    
    df = pd.DataFrame(data)
    return df
