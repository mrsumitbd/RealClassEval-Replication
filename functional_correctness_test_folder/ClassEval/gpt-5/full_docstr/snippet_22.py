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

    @staticmethod
    def _parse_time(t):
        if isinstance(t, str):
            t = t.strip()
            parts = t.split(":")
            if len(parts) != 2:
                raise ValueError("Time must be in H:M or HH:MM format")
            hour = int(parts[0])
            minute = int(parts[1])
        else:
            raise ValueError("Time must be a string")
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            raise ValueError("Hour must be 0-23 and minute 0-59")
        return hour * 60 + minute

    @staticmethod
    def _normalize_course(course):
        if not isinstance(course, dict):
            raise ValueError("course must be a dict")
        name = course.get('name')
        st = course.get('start_time')
        et = course.get('end_time')
        if name is None or st is None or et is None:
            raise ValueError(
                "course must include 'name', 'start_time', and 'end_time'")
        start = Classroom._parse_time(st)
        end = Classroom._parse_time(et)
        if end < start:
            start, end = end, start
        return {
            'name': name,
            'start_time': f"{start // 60:02d}:{start % 60:02d}",
            'end_time': f"{end // 60:02d}:{end % 60:02d}",
            '_start_minutes': start,
            '_end_minutes': end
        }

    def add_course(self, course):
        """
        Add course to self.courses list if the course wasn't in it.
        :param course: dict, information of the course, including 'start_time', 'end_time' and 'name'
        >>> classroom = Classroom(1)
        >>> classroom.add_course({'name': 'math', 'start_time': '8:00', 'end_time': '9:40'})
        """
        norm = self._normalize_course(course)
        # Use display dict without internal keys for external representation,
        # but keep minutes for internal comparisons
        # Ensure uniqueness by comparing public fields
        public_norm = {k: norm[k] for k in ('name', 'start_time', 'end_time')}
        for existing in self.courses:
            if all(existing[k] == public_norm[k] for k in ('name', 'start_time', 'end_time')):
                return
        # store also minutes for efficient checks
        stored = dict(public_norm)
        stored['_start_minutes'] = norm['_start_minutes']
        stored['_end_minutes'] = norm['_end_minutes']
        self.courses.append(stored)

    def remove_course(self, course):
        """
        Remove course from self.courses list if the course was in it.
        :param course: dict, information of the course, including 'start_time', 'end_time' and 'name'
        >>> classroom = Classroom(1)
        >>> classroom.add_course({'name': 'math', 'start_time': '8:00', 'end_time': '9:40'})
        >>> classroom.add_course({'name': 'math', 'start_time': '8:00', 'end_time': '9:40'})
        """
        norm = self._normalize_course(course)
        public_norm = {k: norm[k] for k in ('name', 'start_time', 'end_time')}
        for i, existing in enumerate(self.courses):
            if all(existing[k] == public_norm[k] for k in ('name', 'start_time', 'end_time')):
                self.courses.pop(i)
                return

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
        t = self._parse_time(check_time)
        for c in self.courses:
            if c['_start_minutes'] <= t <= c['_end_minutes']:
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
        norm = self._normalize_course(new_course)
        ns, ne = norm['_start_minutes'], norm['_end_minutes']
        for c in self.courses:
            cs, ce = c['_start_minutes'], c['_end_minutes']
            if not (ne < cs or ns > ce):
                return False
        return True
