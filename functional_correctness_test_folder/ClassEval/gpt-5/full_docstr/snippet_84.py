import sqlite3
from typing import List, Tuple, Dict, Any, Optional


class StudentDatabaseProcessor:
    """
    This is a class with database operation, including inserting student information, searching for student information by name, and deleting student information by name.
    """

    def __init__(self, database_name: str):
        """
        Initializes the StudentDatabaseProcessor object with the specified database name.
        :param database_name: str, the name of the SQLite database.
        """
        self.database_name = database_name

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.database_name)

    def create_student_table(self) -> None:
        """
        Creates a "students" table in the database if it does not exist already.Fields include ID of type int, name of type str, age of type int, gender of type str, and grade of type int
        :return: None
        >>> processor = StudentDatabaseProcessor("students.db")
        >>> processor.create_student_table()
        """
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER,
                    gender TEXT,
                    grade INTEGER
                )
                """
            )
            conn.commit()

    def insert_student(self, student_data: Dict[str, Any]) -> None:
        """
        Inserts a new student into the "students" table.
        :param student_data: dict, a dictionary containing the student's information (name, age, gender, grade).
        :return: None
        >>> processor = StudentDatabaseProcessor("students.db")
        >>> processor.create_student_table()
        >>> student_data = {'name': 'John', 'age': 15, 'gender': 'Male', 'grade': 9}
        >>> processor.insert_student(student_data)
        """
        required_keys = {"name", "age", "gender", "grade"}
        if not required_keys.issubset(student_data.keys()):
            missing = required_keys - set(student_data.keys())
            raise ValueError(
                f"Missing required fields: {', '.join(sorted(missing))}")

        with self._connect() as conn:
            conn.execute(
                "INSERT INTO students (name, age, gender, grade) VALUES (?, ?, ?, ?)",
                (
                    student_data["name"],
                    int(student_data["age"]
                        ) if student_data["age"] is not None else None,
                    student_data["gender"],
                    int(student_data["grade"]
                        ) if student_data["grade"] is not None else None,
                ),
            )
            conn.commit()

    def search_student_by_name(self, name: str) -> List[Tuple]:
        """
        Searches for a student in the "students" table by their name.
        :param name: str, the name of the student to search for.
        :return: list of tuples, the rows from the "students" table that match the search criteria.
        >>> processor = StudentDatabaseProcessor("students.db")
        >>> processor.create_student_table()
        >>> result = processor.search_student_by_name("John")
        """
        with self._connect() as conn:
            cursor = conn.execute(
                "SELECT id, name, age, gender, grade FROM students WHERE name = ?",
                (name,),
            )
            rows = cursor.fetchall()
        return rows

    def delete_student_by_name(self, name: str) -> None:
        """
        Deletes a student from the "students" table by their name.
        :param name: str, the name of the student to delete.
        :return: None
        >>> processor = StudentDatabaseProcessor("students.db")
        >>> processor.create_student_table()
        >>> student_data = {'name': 'John', 'age': 15, 'gender': 'Male', 'grade': 9}
        >>> processor.insert_student(student_data)
        >>> processor.delete_student_by_name("John")
        """
        with self._connect() as conn:
            conn.execute("DELETE FROM students WHERE name = ?", (name,))
            conn.commit()
