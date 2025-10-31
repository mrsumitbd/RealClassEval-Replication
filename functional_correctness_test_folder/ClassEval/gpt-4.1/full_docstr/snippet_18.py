
from datetime import datetime, timedelta


class CalendarUtil:
    """
    This is a class as CalendarUtil that provides functionalities to manage calendar events, schedule appointments, and perform conflict checks.
    """

    def __init__(self):
        """
        Initialize the calendar with an empty list of events.
        """
        self.events = []

    def add_event(self, event):
        """
        Add an event to the calendar.
        :param event: The event to be added to the calendar,dict.
        """
        self.events.append(event)

    def remove_event(self, event):
        """
        Remove an event from the calendar.
        :param event: The event to be removed from the calendar,dict.
        """
        if event in self.events:
            self.events.remove(event)

    def get_events(self, date):
        """
        Get all events on a given date.
        :param date: The date to get events for,datetime.
        :return: A list of events on the given date,list.
        """
        return [e for e in self.events if 'date' in e and e['date'].date() == date.date()]

    def is_available(self, start_time, end_time):
        """
        Check if the calendar is available for a given time slot.
        :param start_time: The start time of the time slot,datetime.
        :param end_time: The end time of the time slot,datetime.
        :return: True if the calendar is available for the given time slot, False otherwise,bool.
        """
        for e in self.events:
            e_start = e.get('start_time', e.get('date'))
            e_end = e.get('end_time')
            if e_start is None or e_end is None:
                continue
            # Check for overlap
            if not (end_time <= e_start or start_time >= e_end):
                return False
        return True

    def get_available_slots(self, date):
        """
        Get all available time slots on a given date.
        :param date: The date to get available time slots for,datetime.
        :return: A list of available time slots on the given date,list.
        """
        # Get all events on the date, sorted by start_time
        events = [e for e in self.events if 'date' in e and e['date'].date()
                  == date.date()]
        slots = []
        if not events:
            # Whole day is available
            start_of_day = datetime(date.year, date.month, date.day, 0, 0)
            end_of_day = start_of_day + timedelta(days=1)
            return [(start_of_day, end_of_day)]
        # Sort events by start_time
        events = sorted(events, key=lambda e: e.get('start_time', e['date']))
        start_of_day = datetime(date.year, date.month, date.day, 0, 0)
        end_of_day = start_of_day + timedelta(days=1)
        prev_end = start_of_day
        for e in events:
            e_start = e.get('start_time', e['date'])
            e_end = e.get('end_time')
            if e_start > prev_end:
                slots.append((prev_end, e_start))
            prev_end = max(prev_end, e_end)
        if prev_end < end_of_day:
            slots.append((prev_end, end_of_day))
        return slots

    def get_upcoming_events(self, num_events):
        """
        Get the next n upcoming events from a given date.
        :param date: The date to get upcoming events from,datetime.
        :param n: The number of upcoming events to get,int.
        :return: A list of the next n upcoming events from the given date,list.
        """
        # Sort events by start_time or date
        def event_sort_key(e):
            return e.get('start_time', e.get('date'))
        sorted_events = sorted(self.events, key=event_sort_key)
        # The docstring and example show that all events are returned if num_events >= len(events)
        # But the example also shows that get_upcoming_events(1) returns 2 events if there are 2 events
        # So, we will return all events if num_events >= len(events), else return first num_events events
        if num_events >= len(sorted_events):
            return sorted_events
        else:
            return sorted_events[:num_events]
