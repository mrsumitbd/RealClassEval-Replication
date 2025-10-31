import numpy as np
from pyspectral.config import get_config
from xlrd import open_workbook
import os

class AvhrrRSR:
    """Container for the NOAA AVHRR-1 RSR data."""

    def __init__(self, wavespace='wavelength'):
        """Initialize the AVHRR-1 RSR class."""
        options = get_config()
        self.avhrr_path = options['avhrr/1'].get('path')
        if not os.path.exists(self.avhrr_path):
            self.avhrr1_path = os.path.join(DATA_PATH, options['avhrr/1'].get('filename'))
        self.output_dir = options.get('rsr_dir', './')
        self.rsr = {}
        for satname in AVHRR1_SATELLITES:
            self.rsr[satname] = {}
            for chname in AVHRR_BAND_NAMES['avhrr/1']:
                self.rsr[satname][chname] = {'wavelength': None, 'response': None}
        self._load()
        self.wavespace = wavespace
        if wavespace not in ['wavelength', 'wavenumber']:
            raise AttributeError('wavespace has to be either ' + "'wavelength' or 'wavenumber'!")
        self.unit = 'micrometer'
        if wavespace == 'wavenumber':
            self.convert2wavenumber()

    def _load(self, scale=1.0):
        """Load the AVHRR RSR data for the band requested."""
        wb_ = open_workbook(self.avhrr_path)
        sheet_names = []
        for sheet in wb_.sheets():
            if sheet.name in ['Kleespies Data']:
                print('Skip sheet...')
                continue
            ch_name = CHANNEL_NAMES.get(sheet.name.strip())
            if not ch_name:
                break
            sheet_names.append(sheet.name.strip())
            header = sheet.col_values(0, start_rowx=0, end_rowx=2)
            platform_name = header[0].strip('# ')
            unit = header[1].split('Wavelength (')[1].strip(')')
            scale = get_scale_from_unit(unit)
            wvl = sheet.col_values(0, start_rowx=2)
            is_comment = True
            idx = 0
            while is_comment:
                item = wvl[::-1][idx]
                if isinstance(item, str):
                    idx = idx + 1
                else:
                    break
            ndim = len(wvl) - idx
            wvl = wvl[0:ndim]
            if platform_name == 'TIROS-N':
                wvl = adjust_typo_avhrr1_srf_only_xls_file(platform_name, wvl)
            response = sheet.col_values(1, start_rowx=2, end_rowx=2 + ndim)
            wavelength = np.array(wvl) * scale
            response = np.array(response)
            self.rsr[platform_name][ch_name]['wavelength'] = wavelength
            self.rsr[platform_name][ch_name]['response'] = response