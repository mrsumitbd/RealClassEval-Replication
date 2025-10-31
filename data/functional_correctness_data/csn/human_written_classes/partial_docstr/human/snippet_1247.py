import os.path
import os
import github3

class GitHubApiUtils:
    """
    Class to query/set GitHub info.
    """

    def __init__(self, owner, repo_name):
        """
        Returns a GitHub object, possibly authed as a user.
        """
        token = os.environ.get('GITHUB_TOKEN', '')
        if len(token):
            self.gh = github3.login(token=token)
        else:
            self.gh = github3.GitHub()
        self.repo = self.gh.repository(owner, repo_name)

    def create_pull(self, *args, **kwargs):
        return self.repo.create_pull(*args, **kwargs)