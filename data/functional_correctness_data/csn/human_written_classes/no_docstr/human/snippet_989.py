class ProjectMetadata:
    project_name = ''
    valid_creds: list[str] = []
    num_repos: int = 0

    def __init__(self, project_name='', valid_creds=[], num_repos=0):
        self.project_name = project_name
        self.valid_creds = valid_creds
        self.num_repos = num_repos

    def __str__(self):
        return f'project {self.project_name} accessible with {self.valid_creds} containing {self.num_repos} repos'