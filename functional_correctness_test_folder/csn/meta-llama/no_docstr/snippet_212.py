
from typing import Dict, Union
from datetime import date
from lunardate import LunarDate


class ThreeNineUtils:

    @staticmethod
    def get_39days(year: int) -> Dict[str, date]:
        """
        Returns a dictionary containing the dates of the three nine days for a given year.

        The three nine days are the third, second, and first nine days of the winter season.
        """
        # Get the winter solstice date
        winter_solstice_date = LunarDate(year, 11, 17).to_solar_date()

        # Initialize the dictionary to store the three nine days
        three_nine_days = {}

        # Calculate the start date of the first nine days
        first_nine_start = winter_solstice_date

        # Calculate the start date of the second nine days
        second_nine_start = first_nine_start + date.resolution * 9

        # Calculate the start date of the third nine days
        third_nine_start = second_nine_start + date.resolution * 9

        # Store the start dates of the three nine days in the dictionary
        three_nine_days['一九'] = first_nine_start
        three_nine_days['二九'] = second_nine_start
        three_nine_days['三九'] = third_nine_start

        return three_nine_days

    @staticmethod
    def get_39label(date_obj: Union[date, LunarDate]) -> str:
        """
        Returns the three nine label for a given date.

        The three nine label is a string indicating which nine days the date falls into.
        """
        # Convert the date object to a solar date if it's a LunarDate object
        if isinstance(date_obj, LunarDate):
            date_obj = date_obj.to_solar_date()

        # Get the winter solstice date of the same year
        winter_solstice_date = LunarDate(date_obj.year, 11, 17).to_solar_date()

        # If the date is before the winter solstice, use the previous year's winter solstice
        if date_obj < winter_solstice_date:
            winter_solstice_date = LunarDate(
                date_obj.year - 1, 11, 17).to_solar_date()

        # Calculate the difference between the date and the winter solstice date
        diff = (date_obj - winter_solstice_date).days

        # Determine the three nine label based on the difference
        if diff < 0:
            return ''
        elif diff < 9:
            return '一九'
        elif diff < 18:
            return '二九'
        elif diff < 27:
            return '三九'
        else:
            return ''
