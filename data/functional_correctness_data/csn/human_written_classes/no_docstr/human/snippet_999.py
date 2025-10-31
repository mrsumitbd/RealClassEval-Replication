class _AppIcon:

    def __init__(self, app, path_to_root, node):
        from aiidalab.app import _AiidaLabApp
        name = app['name']
        app_object = _AiidaLabApp.from_id(name)
        self.logo = app_object.metadata['logo']
        if app_object.is_installed():
            self.link = f"{path_to_root}{app['name']}/{app['notebook']}?{app['parameter_name']}={node.uuid}"
        else:
            self.link = f"{path_to_root}home/single_app.ipynb?app={app['name']}"
        self.description = app['description']

    def to_html_string(self):
        return f'\n            <table style="border-collapse:separate;border-spacing:15px;">\n            <tr>\n                <td style="width:200px"> <a href={self.link!r} target="_blank">  <img src={self.logo!r}> </a></td>\n                <td style="width:800px"> <p style="font-size:16px;">{self.description} </p></td>\n            </tr>\n            </table>\n            '