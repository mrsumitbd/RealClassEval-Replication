class AssessmentSystem:
    """
    This is a class as an student assessment system, which supports add student, add course score, calculate GPA, and other functions for students and courses.
    """

    def __init__(self):
        """
        Initialize the students dict in assessment system.
        """
        self.students = {}

    def add_student(self, name, grade, major):
        """
        Add a new student into self.students dict
        :param name: str, student name
        :param grade: int, student grade
        :param major: str, student major
        >>> system.add_student('student 1', 3, 'SE')
        >>> system.students
        {'student 1': {'name': 'student 1', 'grade': 3, 'major': 'SE', 'courses': {}}}
        """
        if name not in self.students:
            self.students[name] = {
                'name': name,
                'grade': grade,
                'major': major,
                'courses': {}
            }
        else:
            # Update existing student's info but keep courses
            self.students[name]['name'] = name
            self.students[name]['grade'] = grade
            self.students[name]['major'] = major
            if 'courses' not in self.students[name] or not isinstance(self.students[name]['courses'], dict):
                self.students[name]['courses'] = {}

    def add_course_score(self, name, course, score):
        """
        Add score of specific course for student in self.students
        :param name: str, student name
        :param cource: str, cource name
        :param score: int, cource score
        >>> system.add_student('student 1', 3, 'SE')
        >>> system.add_course_score('student 1', 'math', 94)
        >>> system.students
        {'student 1': {'name': 'student 1', 'grade': 3, 'major': 'SE', 'courses': {'math': 94}}}
        """
        if name in self.students:
            if 'courses' not in self.students[name] or not isinstance(self.students[name]['courses'], dict):
                self.students[name]['courses'] = {}
            self.students[name]['courses'][course] = score

    def get_gpa(self, name):
        """
        Get average grade of one student.
        :param name: str, student name
        :return: if name is in students and this students have courses grade, return average grade(float)
                    or None otherwise
        >>> system.add_student('student 1', 3, 'SE')
        >>> system.add_course_score('student 1', 'math', 94)
        >>> system.add_course_score('student 1', 'Computer Network', 92)
        >>> system.get_gpa('student 1')
        93.0

        """
        student = self.students.get(name)
        if not student:
            return None
        courses = student.get('courses', {})
        if not courses:
            return None
        total = sum(courses.values())
        count = len(courses)
        return total / count

    def get_all_students_with_fail_course(self):
        """
        Get all students who have any score blow 60
        :return: list of str ,student name
        >>> system.add_course_score('student 1', 'Society', 59)
        >>> system.get_all_students_with_fail_course()
        ['student 1']
        """
        result = []
        for name, info in self.students.items():
            courses = info.get('courses', {})
            if any(score < 60 for score in courses.values()):
                result.append(name)
        return result

    def get_course_average(self, course):
        """
        Get the average score of a specific course.
        :param course: str, course name
        :return: float, average scores of this course if anyone have score of this course, or None if nobody have records.
        """
        scores = []
        for info in self.students.values():
            courses = info.get('courses', {})
            if course in courses:
                scores.append(courses[course])
        if not scores:
            return None
        return sum(scores) / len(scores)

    def get_top_student(self):
        """
        Calculate every student's gpa with get_gpa method, and find the student with highest gpa
        :return: str, name of student whose gpa is highest
        >>> system.add_student('student 1', 3, 'SE')
        >>> system.add_student('student 2', 2, 'SE')
        >>> system.add_course_score('student 1', 'Computer Network', 92)
        >>> system.add_course_score('student 2', 'Computer Network', 97)
        >>> system.get_top_student()
        'student 2'
        """
        top_name = None
        top_gpa = None
        for name in self.students:
            gpa = self.get_gpa(name)
            if gpa is None:
                continue
            if top_gpa is None or gpa > top_gpa:
                top_gpa = gpa
                top_name = name
        return top_name
