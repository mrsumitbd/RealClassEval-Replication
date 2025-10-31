import logging
import sys

class ReactionProcessor:
    """
        Reaction Processor class. Consumes Reaction Time Series to compute related features.

        These values are recommended by the author of the pilot study :cite:`Kassavetis2015_2`. Check reference         for more details.

        window = 6 #seconds

        :Example:

        >>> import pdkit
        >>> rp = pdkit.ReactionProcessor()
        >>> rs = pdkit.ReactionTimeSeries().load(path_to_data, 'opdc_react')
        >>> rp.extract_features(rs)
    """

    def __init__(self, window=6):
        try:
            self.window = window
            logging.debug('ReactionProcessor init')
        except IOError as e:
            ierr = '({}): {}'.format(e.errno, e.strerror)
            logging.error('ReactionProcessor I/O error %s', ierr)
        except ValueError as verr:
            logging.error('ReactionProcessor ValueError ->%s', verr.message)
        except:
            logging.error('Unexpected error on ReactionProcessor init: %s', sys.exc_info()[0])

    def reaction_times(self, data_frame):
        """
            Computer press, raise and total reaction times.

            :param data_frame: the data frame
            :type data_frame: pandas.DataFrame
            :return press: avg time from button visible until button pressed
            :rtype press: float
            :return raise: avg time from button removed until button released
            :rtype raise: float
            :return total: avg total reaction time
            :rtype total: float

        """
        visibleb = False
        pressed = False
        raised = False
        tmp = []
        for index, row in data_frame.iterrows():
            if not visibleb and row['bVis'] == True:
                start_time_to_press = row['td']
                end_time_to_press = 0
                visibleb = True
                pressed = False
                raised = False
            elif visibleb and (not pressed) and (row['bPres'] == True):
                end_time_to_press = row['td']
                tmp.append(('down', end_time_to_press - start_time_to_press))
                visibleb = True
                pressed = True
                raised = False
            elif visibleb and pressed and (row['bPres'] == True):
                visibleb = True
                pressed = True
                raised = False
            elif visibleb and row['bVis'] == False:
                start_time_to_raise = row['td']
                end_time_to_raise = 0
                visibleb = False
                pressed = False
                raised = False
            elif not visibleb and row['bPres'] == True:
                visibleb = False
                pressed = True
                raised = False
            elif not visibleb and row['bPres'] == False:
                end_time_to_raise = row['td']
                tmp.append(('up', end_time_to_press - start_time_to_press))
                visibleb = False
                pressed = False
                raised = True
            elif visibleb and pressed and (row['bPres'] == False):
                logging.warn('In ReactionProcessor found finger raised in error while button visible. Ignoring action.')
            else:
                logging.warn('In ReactionProcessor invalid finger lift detected. Ignoring action')
        press_t = 0
        raise_t = 0
        length = len(tmp)
        for i in range(length):
            if i % 2 == 0:
                action, time_diff = tmp[i]
                press_t += time_diff
                if i + 1 < length:
                    action, time_diff = tmp[i + 1]
                    raise_t += time_diff
        total = (press_t + raise_t) / length
        press_t /= length
        raise_t /= length
        return (press_t, raise_t, total)

    def extract_features(self, data_frame, pre=''):
        """
            This method extracts all the features available under the Reaction Processor class.

            :param data_frame: the data frame
            :type data_frame: pandas.DataFrame
            :return: 'frequency', 'moving_frequency','continuous_frequency','mean_moving_time','incoordination_score',                     'mean_alnt_target_distance','kinesia_scores', 'akinesia_times','dysmetria_score'
            :rtype: list

        """
        try:
            p, r, t = self.reaction_times(data_frame)
            return {pre + 'mean_press_button_time': p, pre + 'mean_release_button_time': r, pre + 'mean_total_reaction_time': t}
        except:
            logging.error('Error in ReactionProcessor while extracting features: %s', sys.exc_info()[0])