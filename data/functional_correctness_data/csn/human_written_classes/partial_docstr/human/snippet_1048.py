from pdkit.utils import load_data
import logging
import sys

class TremorTimeSeries:
    """
        This is a wrapper class to load the Tremor Time Series data.
    """

    def __init__(self):
        logging.debug('TremorTimeSeries init')

    def load(self, filename, format_file='cloudupdrs'):
        """
            This is a general load data method where the format of data to load can be passed as a parameter,

            :param str filename: The path to load data from
            :param str format_file: format of the file. Default is CloudUPDRS. Set to mpower for mpower data.
            :return dataframe: data_frame.x, data_frame.y, data_frame.z: x, y, z components of the acceleration             data_frame.index is the datetime-like index
        """
        try:
            ts = load_data(filename, format_file)
            validator = CloudUPDRSDataFrameValidator()
            if validator.is_valid(ts):
                return ts
            else:
                logging.error('Error loading data, wrong format.')
                return None
        except IOError as e:
            ierr = '({}): {}'.format(e.errno, e.strerror)
            logging.error('load data, file not found, I/O error %s', ierr)
        except ValueError as verr:
            logging.error('load data ValueError ->%s', verr.message)
        except:
            logging.error('Unexpected error on load data method: %s', sys.exc_info()[0])