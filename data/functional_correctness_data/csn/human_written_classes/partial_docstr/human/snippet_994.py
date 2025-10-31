from pymagicc.errors import InvalidTemporalResError
import pandas as pd
from pymagicc.definitions import convert_magicc6_to_magicc7_variables, convert_magicc7_to_openscm_variables, convert_magicc_to_openscm_regions
import numpy as np

class _LegacyBinFormat:
    version = None

    @staticmethod
    def process_header(reader, stream):
        metadata = {'datacolumns': stream.read_chunk('I'), 'firstyear': stream.read_chunk('I'), 'lastyear': stream.read_chunk('I'), 'annualsteps': stream.read_chunk('I')}
        if metadata['annualsteps'] != 1:
            raise InvalidTemporalResError('{}: Only annual files can currently be processed'.format(reader.filepath))
        return metadata

    @staticmethod
    def process_data(reader, stream, metadata):
        """
        Extract the tabulated data from the input file

        # Arguments
        stream (Streamlike object): A Streamlike object (nominally StringIO)
            containing the table to be extracted
        metadata (dict): metadata read in from the header and the namelist

        # Returns
        df (pandas.DataFrame): contains the data, processed to the standard
            MAGICCData format
        metadata (dict): updated metadata based on the processing performed
        """
        index = np.arange(metadata['firstyear'], metadata['lastyear'] + 1)
        globe = stream.read_chunk('d')
        if not len(globe) == len(index):
            raise AssertionError("Length of data doesn't match length of index: {} != {}".format(len(globe), len(index)))
        if metadata['datacolumns'] == 1:
            num_boxes = 0
            data = globe[:, np.newaxis]
            regions = ['World']
        else:
            regions = stream.read_chunk('d')
            num_boxes = int(len(regions) / len(index))
            regions = regions.reshape((-1, num_boxes), order='F')
            data = np.concatenate((globe[:, np.newaxis], regions), axis=1)
            regions = ['World', 'World|Northern Hemisphere|Ocean', 'World|Northern Hemisphere|Land', 'World|Southern Hemisphere|Ocean', 'World|Southern Hemisphere|Land']
        df = pd.DataFrame(data, index=index)
        if pd.api.types.is_float_dtype(df.index):
            df.index = df.index.to_series().round(3)
        df.index.name = 'time'
        variable = convert_magicc6_to_magicc7_variables(reader._get_variable_from_filepath())
        variable = convert_magicc7_to_openscm_variables(variable)
        column_headers = {'variable': [variable] * (num_boxes + 1), 'region': regions, 'unit': 'unknown'}
        return (df, metadata, column_headers)