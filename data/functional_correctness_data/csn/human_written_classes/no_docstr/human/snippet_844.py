from crispy.config import Config as _Config

class Config:

    def default(self):
        settings = _Config()
        settings.default()

    def set_setting(self, name, value):
        if name == 'Shift Spectra':
            name = 'ShiftSpectra'
        elif name == 'Remove Files':
            name = 'RemoveFiles'
        else:
            print(f'Unknown setting: {name}')
            return
        settings = _Config().read()
        settings.setValue(f'Quanty/{name}', value)
        settings.sync()