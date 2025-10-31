import sys
import os.path
import json
import matplotlib.pyplot as plt
import matplotlib.colors
import matplotlib

class Colormap:

    def __init__(self, cmtype, method, uniform_space):
        self.can_edit = True
        self.params = {}
        self.cmtype = cmtype
        self.method = method
        self.name = None
        self.cmap = None
        self.uniform_space = uniform_space
        if self.uniform_space == 'buggy-CAM02-UCS':
            self.uniform_space = buggy_CAM02UCS

    def load(self, path):
        self.path = path
        if os.path.isfile(path):
            _, extension = os.path.splitext(path)
            if extension == '.py':
                self.can_edit = True
                self.cmtype = 'linear'
                self.method = 'Bezier'
                ns = {'__name__': '', '__file__': os.path.basename(self.path)}
                with open(self.path) as f:
                    code = compile(f.read(), os.path.basename(self.path), 'exec')
                    exec(code, globals(), ns)
                self.params = ns.get('parameters', {})
                if not self.params:
                    self.can_edit = False
                if 'min_JK' in self.params:
                    self.params['min_Jp'] = self.params.pop('min_JK')
                    self.params['max_Jp'] = self.params.pop('max_JK')
                self.cmap = ns.get('test_cm', None)
                self.name = self.cmap.name
            elif extension == '.jscm':
                self.can_edit = False
                with open(self.path) as f:
                    data = json.loads(f.read())
                    self.name = data['name']
                    colors = data['colors']
                    colors = [colors[i:i + 6] for i in range(0, len(colors), 6)]
                    colors = [[int(c[2 * i:2 * i + 2], 16) / 255 for i in range(3)] for c in colors]
                    self.cmap = matplotlib.colors.ListedColormap(colors, self.name)
                    if 'extensions' in data and 'https://matplotlib.org/viscm' in data['extensions']:
                        self.can_edit = True
                        self.params = {k: v for k, v in data['extensions']['https://matplotlib.org/viscm'].items() if k in {'xp', 'yp', 'min_Jp', 'max_Jp', 'fixed', 'filter_k', 'uniform_space'}}
                        self.params['name'] = self.name
                        self.cmtype = data['extensions']['https://matplotlib.org/viscm']['cmtype']
                        self.method = data['extensions']['https://matplotlib.org/viscm']['spline_method']
                        self.uniform_space = data['extensions']['https://matplotlib.org/viscm']['uniform_colorspace']
            else:
                sys.exit('Unsupported filetype')
        else:
            self.can_edit = False
            self.cmap = lookup_colormap_by_name(path)
            self.name = path