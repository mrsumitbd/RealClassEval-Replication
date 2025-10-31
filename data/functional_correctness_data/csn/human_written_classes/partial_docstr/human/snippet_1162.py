import logging
import xmltodict
from os.path import join
from os import getcwd

class IARDefinitions:

    def _get_option(self, settings, find_key):
        for option in settings:
            if option['name'] == find_key:
                return settings.index(option)

    def get_mcu_definition(self, project_file):
        """ Parse project file to get mcu definition """
        project_file = join(getcwd(), project_file)
        ewp_dic = xmltodict.parse(open(project_file, 'rb'), dict_constructor=dict)
        mcu = MCU_TEMPLATE
        try:
            ewp_dic['project']['configuration']
        except KeyError:
            logging.debug('The project_file %s seems to be not valid .ewp file.')
            return mcu
        mcu['tool_specific'] = {'iar': {'OGChipSelectEditMenu': {'state': []}, 'OGCoreOrChip': {'state': [1]}}}
        try:
            index_general = self._get_option(ewp_dic['project']['configuration'][0]['settings'], 'General')
            configuration = ewp_dic['project']['configuration'][0]
        except KeyError:
            index_general = self._get_option(ewp_dic['project']['configuration']['settings'], 'General')
            configuration = ewp_dic['project']['configuration']
        index_option = self._get_option(configuration['settings'][index_general]['data']['option'], 'OGChipSelectEditMenu')
        OGChipSelectEditMenu = configuration['settings'][index_general]['data']['option'][index_option]
        mcu['tool_specific']['iar']['OGChipSelectEditMenu']['state'].append(OGChipSelectEditMenu['state'].replace('\t', ' ', 1))
        fileVersion = 1
        try:
            if self._get_option(configuration['settings'][index_general]['data']['option'], 'FPU2'):
                fileVersion = 2
        except TypeError:
            pass
        index_option = self._get_option(configuration['settings'][index_general]['data']['option'], 'GBECoreSlave')
        GBECoreSlave = configuration['settings'][index_general]['data']['option'][index_option]
        mcu['tool_specific']['iar']['GBECoreSlave'] = {'state': [int(GBECoreSlave['state'])]}
        if fileVersion == 2:
            index_option = self._get_option(configuration['settings'][index_general]['data']['option'], 'GFPUCoreSlave2')
            GFPUCoreSlave2 = configuration['settings'][index_general]['data']['option'][index_option]
            mcu['tool_specific']['iar']['GFPUCoreSlave2'] = {'state': [int(GFPUCoreSlave2['state'])]}
            index_option = self._get_option(configuration['settings'][index_general]['data']['option'], 'CoreVariant')
            CoreVariant = configuration['settings'][index_general]['data']['option'][index_option]
            try:
                mcu['tool_specific']['iar']['CoreVariant'] = {'state': [int(CoreVariant['state'])]}
            except TypeError:
                pass
        else:
            index_option = self._get_option(configuration['settings'][index_general]['data']['option'], 'GFPUCoreSlave')
            GFPUCoreSlave = configuration['settings'][index_general]['data']['option'][index_option]
            mcu['tool_specific']['iar']['GFPUCoreSlave'] = {'state': [int(GFPUCoreSlave['state'])]}
            index_option = self._get_option(configuration['settings'][index_general]['data']['option'], 'Variant')
            Variant = configuration['settings'][index_general]['data']['option'][index_option]
            mcu['tool_specific']['iar']['Variant'] = {'state': [int(Variant['state'])]}
        return mcu