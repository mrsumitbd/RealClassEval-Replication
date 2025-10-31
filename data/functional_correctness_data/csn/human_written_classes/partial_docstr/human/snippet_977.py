from aerofiles.util.timezone import TimeZoneFix
import datetime

class Reader:
    """
    A reader for the IGC flight log file format.

    skip_duplicates flag removes trailing duplicate time entries

    Example:

    .. sourcecode:: python

        >>> with open('track.igc', 'r') as f:
        ...     parsed = Reader(skip_duplicates=True).read(f)

    """

    def __init__(self, skip_duplicates=False):
        self.reader = None
        self.skip_duplicates = skip_duplicates

    def read(self, file_obj):
        """
        Read the specified file object and return a dictionary with the parsed data.

        :param file_obj: a Python file object

        """
        self.reader = LowLevelReader(file_obj)
        logger_id = [[], None]
        fix_records = [[], []]
        task = [[], {'waypoints': []}]
        dgps_records = [[], []]
        event_records = [[], []]
        satellite_records = [[], []]
        security_records = [[], []]
        header = [[], {}]
        fix_record_extensions = [[], []]
        k_record_extensions = [[], []]
        k_records = [[], []]
        comment_records = [[], []]
        for record_type, line, error in self.reader:
            if record_type == 'A':
                if error:
                    logger_id[0].append(error)
                else:
                    logger_id[1] = line
            elif record_type == 'B':
                if error:
                    if MissingRecordsError not in fix_records[0]:
                        fix_records[0].append(MissingRecordsError)
                else:
                    if len(fix_record_extensions[0]) > 0 and MissingExtensionsError not in fix_records[0]:
                        fix_records[0].append(MissingExtensionsError)
                    fix_record = LowLevelReader.process_B_record(line, fix_record_extensions[1])
                    if len(fix_records[1]) == 0:
                        date = header[1]['utc_date']
                    else:
                        previous_fix = fix_records[1][-1]
                        date = previous_fix['datetime'].date()
                        time = previous_fix['datetime'].time()
                        if fix_record['time'] < time:
                            date = date + datetime.timedelta(days=1)
                        if fix_record['time'] == time and self.skip_duplicates:
                            continue
                    fix_record['datetime'] = datetime.datetime.combine(date, fix_record['time']).replace(tzinfo=TimeZoneFix(0))
                    if 'time_zone_offset' in header[1]:
                        timezone = TimeZoneFix(header[1]['time_zone_offset'])
                        fix_record['datetime_local'] = fix_record['datetime'].astimezone(timezone)
                    fix_records[1].append(fix_record)
            elif record_type == 'C':
                task_item = line
                if error:
                    if MissingRecordsError not in task[0]:
                        task[0].append(MissingRecordsError)
                elif task_item['subtype'] == 'task_info':
                    del task_item['subtype']
                    task[1]['waypoints'] = []
                    task[1].update(task_item)
                elif task_item['subtype'] == 'waypoint_info':
                    del task_item['subtype']
                    task[1]['waypoints'].append(task_item)
            elif record_type == 'D':
                if error:
                    if MissingRecordsError not in dgps_records[0]:
                        dgps_records[0].append(MissingRecordsError)
                else:
                    dgps_records[1].append(line)
            elif record_type == 'E':
                if error:
                    if MissingRecordsError not in event_records[0]:
                        event_records[0].append(MissingRecordsError)
                else:
                    event_records[1].append(line)
            elif record_type == 'F':
                if error:
                    if MissingRecordsError not in satellite_records[0]:
                        satellite_records[0].append(MissingRecordsError)
                else:
                    satellite_records[1].append(line)
            elif record_type == 'G':
                if error:
                    if MissingRecordsError not in security_records[0]:
                        security_records[0].append(MissingRecordsError)
                else:
                    security_records[1].append(line)
            elif record_type == 'H':
                header_item = line
                if error:
                    if MissingRecordsError not in header[0]:
                        header[0].append(MissingRecordsError(error))
                else:
                    del header_item['source']
                    header[1].update(header_item)
            elif record_type == 'I':
                if error:
                    fix_record_extensions[0].append(error)
                else:
                    fix_record_extensions[1] = line
            elif record_type == 'J':
                if error:
                    k_record_extensions[0].append(error)
                else:
                    k_record_extensions[1] = line
            elif record_type == 'K':
                if error:
                    if MissingRecordsError not in k_records[0]:
                        k_records[0].append(MissingRecordsError)
                else:
                    if len(k_record_extensions[0]) > 0 and MissingExtensionsError not in k_records[0]:
                        k_records[0].append(MissingExtensionsError)
                    k_record = LowLevelReader.process_K_record(line, k_record_extensions[1])
                    k_records[1].append(k_record)
            elif record_type == 'L':
                if error:
                    if MissingRecordsError not in comment_records[0]:
                        comment_records[0].append(MissingRecordsError)
                else:
                    comment_records[1].append(line)
        return dict(logger_id=logger_id, fix_records=fix_records, task=task, dgps_records=dgps_records, event_records=event_records, satellite_records=satellite_records, security_records=security_records, header=header, fix_record_extensions=fix_record_extensions, k_record_extensions=k_record_extensions, k_records=k_records, comment_records=comment_records)