
from datetime import datetime


class Classroom:
    """
    This is a class representing a classroom, capable of adding and removing courses, checking availability at a given time, and detecting conflicts when scheduling new courses.
    """

    def __init__(self, id):
        """
        Initialize the classroom management system.
        :param id: int, the id of classroom
        """
        self.id = id
        self.courses = []

    def add_course(self, course):
        """
        Add course to self.courses list if the course wasn't in it.
        :param course: dict, information of the course, including 'start_time', 'end_time' and 'name'
        """
        if course not in self.courses:
            self.courses.append(course)

    def remove_course(self, course):
        """
        Remove course from self.courses list if the course was in it.
        :param course: dict, information of the course, including 'start_time', 'end_time' and 'name'
        """
        if course in self.courses:
            self.courses.remove(course)

    def is_free_at(self, check_time):
        """
        change the time format as '%H:%M' and check the time is free or not in the classroom.
        :param check_time: str, the time need to be checked
        :return: True if the check_time does not conflict with every course time, or False otherwise.
        """
        check_dt = datetime.strptime(check_time, '%H:%M')
        for course in self.courses:
            start_dt = datetime.strptime(course['start_time'], '%H:%M')
            end_dt = datetime.strptime(course['end_time'], '%H:%M')
            if start_dt <= check_dt < end_dt:
                return False
        return True

    def check_course_conflict(self, new_course):
        """
        Before adding a new course, check if the new course time conflicts with any other course.
        :param new_course: dict, information of the course, including 'start_time', 'end_time' and 'name'
        :return: False if the new course time conflicts(including two courses have the same boundary time) with other courses, or True otherwise.
        """
        new_start = datetime.strptime(new_course['start_time'], '%H:%M')
        new_end = datetime.strptime(new_course['end_time'], '%H:%M')
        for course in self.courses:
            start = datetime.strptime(course['start_time'], '%H:%M')
            end = datetime.strptime(course['end_time'], '%H:%M')
            # Conflict if intervals overlap or touch at the boundary
            if not (new_end <= start or new_start >= end):
                return False
            # Also conflict if boundaries touch (e.g., new_end == start or new_start == end)
            if new_end == start or new_start == end:
                return False
        return True
