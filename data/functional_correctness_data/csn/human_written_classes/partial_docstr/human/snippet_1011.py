import os
import re
from opyplus.conf import CONF

class Mtd:
    """
    Class describing an EnergyPlus .mtd file.

    Parameters
    ----------
    path: str
        Path to the EnergyPlus .mtd file
    """

    def __init__(self, path):
        if not os.path.isfile(path):
            raise FileNotFoundError("No file at given path: '%s'." % path)
        self._path = path
        self._variables_d, self._meters_d = self._parse()

    def _parse(self):
        variables_d = {}
        meters_d = {}
        output_l, current, current_s = (None, None, None)
        var_pattern = '^ Meters for (\\d*),([^\\[\\]]*) \\[([\\w\\d]*)\\]$'
        meter_pattern = '^ For Meter=([^\\[\\]]*) \\[([\\w\\d]*)],(.*)$'
        with open(self._path, 'r', encoding=CONF.encoding) as f:
            for line_s in f:
                if line_s == '\n':
                    if output_l is None:
                        output_l = []
                    else:
                        output_l.append([current, current_s])
                    current, current_s = (None, '')
                    continue
                if current is None:
                    match = re.search(var_pattern, line_s)
                    if match is not None:
                        current = Variable(match.group(2), int(match.group(1)), match.group(3))
                        variables_d[current.ref] = current
                    else:
                        match = re.search(meter_pattern, line_s)
                        if match is None:
                            raise RuntimeError("Line was not parsed correctly: '%s'." % line_s)
                        kwargs = {}
                        for kv in line_s.split(',')[:-1]:
                            k, v = kv.split('=')
                            kwargs[k] = v
                        current = Meter(match.group(1), match.group(2), **kwargs)
                        meters_d[current.ref] = current
                else:
                    current_s += line_s
        meter_pattern = '^  OnMeter=([^\\[\\]]*) \\[[\\w\\d]*\\]$'
        var_pattern = '^  (.*)$'
        for k, v in output_l:
            if isinstance(k, Variable):
                for v_s in v.split('\n')[:-1]:
                    match = re.search(meter_pattern, v_s)
                    if match is None:
                        raise RuntimeError("Meter pattern not parsed: '%s'." % v_s)
                    k.link_meter(meters_d[match.group(1)])
            else:
                for v_s in v.split('\n')[:-1]:
                    match = re.search(var_pattern, v_s)
                    if match is None:
                        raise RuntimeError("Variable pattern not parsed: '%s'." % v_s)
                    k.link_variable(variables_d[match.group(1)])
        return (variables_d, meters_d)

    def get_variable_refs(self, meter_ref):
        """
        Get variable refs corresponding to a certain meter reference.

        Parameters
        ----------
        meter_ref: str
            The meter reference

        Returns
        -------
        list of str
        """
        return [v.table_ref for v in self._meters_d[meter_ref].variables_l]

    def has_meter(self, meter_ref):
        """
        Check whether the mtd file has a certain meter.

        Parameters
        ----------
        meter_ref: str
            Ref of the meter

        Returns
        -------
        bool
        """
        return meter_ref in self._meters_d