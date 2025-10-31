
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
        >>> classroom = Classroom(1)
        >>> classroom.add_course({'name': 'math', 'start_time': '8:00', 'end_time': '9:40'})
        """
        if course not in self.courses:
            self.courses.append(course)

    def remove_course(self, course):
        """
        Remove course from self.courses list if the course was in it.
        :param course: dict, information of the course, including 'start_time', 'end_time' and 'name'
        >>> classroom = Classroom(1)
        >>> classroom.add_course({'name': 'math', 'start_time': '8:00', 'end_time': '9:40'})
        >>> classroom.add_course({'name': 'math', 'start_time': '8:00', 'end_time': '9:40'})
        """
        if course in self.courses:
            self.courses.remove(course)

    def is_free_at(self, check_time):
        """
        change the time format as '%H:%M' and check the time is free or not in the classroom.
        :param check_time: str, the time need to be checked
        :return: True if the check_time does not conflict with every course time, or False otherwise.
        >>> classroom = Classroom(1)
        >>> classroom.add_course({'name': 'math', 'start_time': '8:00', 'end_time': '9:40'})
        >>> classroom.is_free_at('10:00')
        True
        >>> classroom.is_free_at('9:00')
        False
        """
        check_h, check_m = map(int, check_time.split(':'))
        check_total = check_h * 60 + check_m
        for course in self.courses:
            start_h, start_m = map(int, course['start_time'].split(':'))
            end_h, end_m = map(int, course['end_time'].split(':'))
            start_total = start_h * 60 + start_m
            end_total = end_h * 60 + end_m
            if start_total <= check_total <= end_total:
                return False
        return True

    def check_course_conflict(self, new_course):
        """
        Before adding a new course, check if the new course time conflicts with any other course.
        :param new_course: dict, information of the course, including 'start_time', 'end_time' and 'name'
        :return: False if the new course time conflicts(including two courses have the same boundary time) with other courses, or True otherwise.
        >>> classroom = Classroom(1)
        >>> classroom.add_course({'name': 'math', 'start_time': '8:00', 'end_time': '9:40'})
        >>> classroom.check_course_conflict({'name': 'SE', 'start_time': '9:40', 'end_time': '10:40'})
        False
        """
        new_start_h, new_start_m = map(
            int, new_course['start_time'].split(':'))
        new_end_h, new_end_m = map(int, new_course['end_time'].split(':'))
        new_start_total = new_start_h * 60 + new_start_m
        new_end_total = new_end_h * 60 + new_end_m
        for course in self.courses:
            start_h, start_m = map(int, course['start_time'].split(':'))
            end_h, end_m = map(int, course['end_time'].split(':'))
            start_total = start_h * 60 + start_m
            end_total = end_h * 60 + end_m
            if not (new_end_total <= start_total or new_start_total >= end_total):
                return False
        return True
