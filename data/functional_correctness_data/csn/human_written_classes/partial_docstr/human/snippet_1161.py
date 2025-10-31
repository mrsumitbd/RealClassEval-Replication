from os.path import join
from os import getcwd
import xmltodict

class CoIDEdefinitions:

    def _coproj_find_option(self, option_dic, key_to_find, value_to_match):
        i = 0
        for option in option_dic:
            for k, v in option.items():
                if k == key_to_find and value_to_match == v:
                    return i
            i += 1
        return None

    def get_mcu_definition(self, project_file):
        """ Parse project file to get mcu definition """
        project_file = join(getcwd(), project_file)
        coproj_dic = xmltodict.parse(open(project_file, 'rb'), dict_constructor=dict)
        mcu = MCU_TEMPLATE
        IROM1_index = self._coproj_find_option(coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'], '@name', 'IROM1')
        IROM2_index = self._coproj_find_option(coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'], '@name', 'IROM2')
        IRAM1_index = self._coproj_find_option(coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'], '@name', 'IRAM1')
        IRAM2_index = self._coproj_find_option(coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'], '@name', 'IRAM2')
        defaultAlgorithm_index = self._coproj_find_option(coproj_dic['Project']['Target']['DebugOption']['Option'], '@name', 'org.coocox.codebugger.gdbjtag.core.defaultAlgorithm')
        mcu['tool_specific'] = {'coide': {'Device': {'manufacturerId': [coproj_dic['Project']['Target']['Device']['@manufacturerId']], 'manufacturerName': [coproj_dic['Project']['Target']['Device']['@manufacturerName']], 'chipId': [coproj_dic['Project']['Target']['Device']['@chipId']], 'chipName': [coproj_dic['Project']['Target']['Device']['@chipName']]}, 'DebugOption': {'defaultAlgorithm': [coproj_dic['Project']['Target']['DebugOption']['Option'][defaultAlgorithm_index]['@value']]}, 'MemoryAreas': {'IROM1': {'name': [coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'][IROM1_index]['@name']], 'size': [coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'][IROM1_index]['@size']], 'startValue': [coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'][IROM1_index]['@startValue']], 'type': [coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'][IROM1_index]['@type']]}, 'IRAM1': {'name': [coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'][IRAM1_index]['@name']], 'size': [coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'][IRAM1_index]['@size']], 'startValue': [coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'][IRAM1_index]['@startValue']], 'type': [coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'][IRAM1_index]['@type']]}, 'IROM2': {'name': [coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'][IROM2_index]['@name']], 'size': [coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'][IROM2_index]['@size']], 'startValue': [coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'][IROM2_index]['@startValue']], 'type': [coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'][IROM2_index]['@type']]}, 'IRAM2': {'name': [coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'][IRAM2_index]['@name']], 'size': [coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'][IRAM2_index]['@size']], 'startValue': [coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'][IRAM2_index]['@startValue']], 'type': [coproj_dic['Project']['Target']['BuildOption']['Link']['MemoryAreas']['Memory'][IRAM2_index]['@type']]}}}}
        return mcu