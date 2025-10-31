from os.path import normpath, join, pardir, sep
import os

class ProjectSettings:
    PROJECT_ROOT = os.environ.get('PROJECT_GENERATOR_ROOT') or join(pardir, pardir)
    DEFAULT_TOOL = os.environ.get('PROJECT_GENERATOR_DEFAULT_TOOL') or 'uvision'
    DEFAULT_EXPORT_LOCATION_FORMAT = join('generated_projects', '{tool}_{project_name}')
    DEFAULT_ROOT = os.getcwd()

    def __init__(self):
        """ This are default enviroment settings for build tools. To override,
        define them in the projects.yaml file. """
        self.paths = {}
        self.templates = {}
        self.paths['uvision'] = os.environ.get('UV4') or join('C:', sep, 'Keil', 'UV4', 'UV4.exe')
        self.paths['iar'] = os.environ.get('IARBUILD') or join('C:', sep, 'Program Files (x86)', 'IAR Systems', 'Embedded Workbench 7.0', 'common', 'bin')
        self.paths['gcc'] = os.environ.get('ARM_GCC_PATH') or ''
        self.export_location_format = self.DEFAULT_EXPORT_LOCATION_FORMAT
        self.root = os.getcwd()

    def update(self, settings):
        if settings:
            if 'tools' in settings:
                for k, v in settings['tools'].items():
                    if k in self.paths:
                        if 'path' in v.keys():
                            self.paths[k] = v['path'][0]
                    if 'template' in v.keys():
                        self.templates[k] = v['template']
            if 'export_dir' in settings:
                self.export_location_format = normpath(settings['export_dir'][0])
            if 'root' in settings:
                self.root = normpath(settings['root'][0])

    def get_env_settings(self, env_set):
        return self.paths[env_set]