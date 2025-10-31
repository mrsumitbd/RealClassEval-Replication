import logging
import sys
from pdkit.utils import load_data

class ReactionTimeSeries:
    """
        This is a wrapper class to load the Reaction Time Series data.
    """

    def __init__(self):
        logging.debug('ReactionTimeSeries init')

    def load(self, filename, format_file='opdc_react', button_left_rect=None, button_right_rect=None):
        """
            This is a general load data method where the format of data to load can be passed as a parameter,

            :param str filename: The path to load data from
            :param str format_file: format of the file. Default is CloudUPDRS. Set to mpower for mpower data.
            :return dataframe: data_frame.x, data_frame.y: components of tapping position. data_frame.x_target,             data_frame.y_target their target. data_frame.index is the datetime-like index
        """
        try:
            ts = load_data(filename, format_file, button_left_rect, button_right_rect)
            "\n            if format_file == 'opdc_react':\n                validator = ReactOPDCDataFrameValidator()\n            else:\n                logging.error('File format error, format file type provided is not valid for reaction tests.')\n                return None\n\n            if validator.is_valid(ts):\n                return ts.fillna(0)\n            else:\n                logging.error('Validator error loading data, wrong format.')\n                return None\n            "
            return ts.fillna(0)
        except IOError as e:
            ierr = '({}): {}'.format(e.errno, e.strerror)
            logging.error('load data, file not found, I/O error %s', ierr)
        except ValueError as verr:
            logging.error('load data ValueError ->%s', verr.message)
        except:
            logging.error('Unexpected error on load data method: %s', sys.exc_info()[0])