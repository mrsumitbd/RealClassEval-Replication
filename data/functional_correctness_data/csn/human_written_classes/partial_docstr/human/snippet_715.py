import json

class NotebookSession:
    """Representation of session info returned by the notebook's /api/sessions/ endpoint.

    Attributes
    ----------
    id: str
    path: str 
    name: str 
    type: str 
    kernel: KernelInfo
    notebook: dict 
    model: dict
        Record of the raw response (without converting the KernelInfo).

    Example
    -------
    ::

        {id: '68d9c58f-c57d-4133-8b41-5ec2731b268d',
         path: 'Untitled38.ipynb',
         name: '',
         type: 'notebook',
         kernel: KernelInfo(id='f92b7c8b-0858-4d10-903c-b0631540fb36', 
                            name='dev', 
                            last_activity='2019-03-14T23:38:08.137987Z', 
                            execution_state='idle', 
                            connections=0),
        notebook: {'path': 'Untitled38.ipynb', 'name': ''}}
    """

    def __init__(self, *args, path, name, type, kernel, notebook={}, **kwargs):
        self.model = {'path': path, 'name': name, 'type': type, 'kernel': kernel, 'notebook': notebook}
        self.path = path
        self.name = name
        self.type = type
        self.kernel = KernelInfo(**kernel)
        self.notebook = notebook

    def __repr__(self):
        return json.dumps(self.model, indent=2)

    def __eq__(self, other):
        if isinstance(other, NotebookSession):
            cmp_attrs = [self.path == other.path, self.name == other.name, self.type == other.type, self.kernel == other.kernel, self.notebook == other.notebook]
            return all(cmp_attrs)
        else:
            return False