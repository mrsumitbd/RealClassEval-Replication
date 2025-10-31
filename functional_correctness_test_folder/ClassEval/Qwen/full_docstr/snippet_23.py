
class ClassRegistrationSystem:
    """
    This is a class as a class registration system, allowing to register students, register them for classes, retrieve students by major, get a list of all majors, and determine the most popular class within a specific major.
    """

    def __init__(self):
        """
        Initialize the registration system with the attribute students and students_registration_class.
        students is a list of student dictionaries, each student dictionary has the key of name and major.
        students_registration_class is a dictionaries, key is the student name, value is a list of class names
        """
        self.students = []
        self.students_registration_classes = {}

    def register_student(self, student):
        """
        register a student to the system, add the student to the students list, if the student is already registered, return 0, else return 1
        """
        if any(s['name'] == student['name'] for s in self.students):
            return 0
        self.students.append(student)
        self.students_registration_classes[student['name']] = []
        return 1

    def register_class(self, student_name, class_name):
        """
        register a class to the student.
        :param student_name: str
        :param class_name: str
        :return a list of class names that the student has registered
        """
        if student_name in self.students_registration_classes:
            if class_name not in self.students_registration_classes[student_name]:
                self.students_registration_classes[student_name].append(
                    class_name)
        return self.students_registration_classes.get(student_name, [])

    def get_students_by_major(self, major):
        """
        get all students in the major
        :param major: str
        :return a list of student name
        """
        return [s['name'] for s in self.students if s['major'] == major]

    def get_all_major(self):
        """
        get all majors in the system
        :return a list of majors
        """
        return list(set(s['major'] for s in self.students))

    def get_most_popular_class_in_major(self, major):
        """
        get the class with the highest enrollment in the major.
        :return  a string of the most popular class in this major
        """
        from collections import defaultdict

        major_students = [s['name']
                          for s in self.students if s['major'] == major]
        class_counts = defaultdict(int)

        for student in major_students:
            for class_name in self.students_registration_classes.get(student, []):
                class_counts[class_name] += 1

        if not class_counts:
            return None

        return max(class_counts, key=class_counts.get)
