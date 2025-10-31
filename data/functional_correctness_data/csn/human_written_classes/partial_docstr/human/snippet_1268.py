import datetime

class MissionTime:
    """
    Represents date and time in a mission
    """

    def __init__(self, moment: datetime.datetime) -> None:
        self.date = datetime.date(moment.year, moment.month, moment.day)
        self.mission_start_time = moment.hour * 3600 + moment.minute * 60 + moment.second
        self.time = datetime.time(hour=moment.hour, minute=moment.minute, second=moment.second)
        self.datetime = datetime.datetime.combine(self.date, self.time)

    def apply_to_miz(self, miz):
        """
        Applies this datetime to a Miz object (it will be mutated in place)

        Args:
            miz: MIZ object to mutate

        Returns: True

        """
        miz.mission.day = self.date.day
        miz.mission.month = self.date.month
        miz.mission.year = self.date.year
        miz.mission.mission_start_time = self.mission_start_time
        return True

    @staticmethod
    def from_string(input_str) -> 'MissionTime':
        """
        Creates a MissionTime instance from a string

        Format: YYYYMMDDHHMMSS

        Args:
            input_str: string to parse

        Returns: MissionTime instance

        """
        match = RE_INPUT_STRING.match(input_str)
        if not match:
            raise ValueError(f'badly formatted date/time: {input_str}')
        return MissionTime(datetime.datetime(int(match.group('year')), int(match.group('month')), int(match.group('day')), int(match.group('hour')), int(match.group('minute')), int(match.group('second'))))

    @staticmethod
    def now() -> 'MissionTime':
        """

        Returns: MissionTime object with the current time

        """
        return MissionTime(datetime.datetime.now())