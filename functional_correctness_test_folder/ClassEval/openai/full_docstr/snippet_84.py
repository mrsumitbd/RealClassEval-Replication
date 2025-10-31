
import sqlite3
from typing import List, Tuple, Dict


class StudentDatabaseProcessor:
    """
    This is a class with database operation, including inserting student information,
    searching for student information by name, and deleting student information by name.
    """

    def __init__(self, database_name: str):
        """
        Initializes the StudentDatabaseProcessor object with the specified database name.
        :param database_name: str, the name of the SQLite database.
        """
        self.database_name = database_name

    def _get_connection(self):
        """Internal helper to get a new database connection."""
        return sqlite3.connect(self.database_name)

    def create_student_table(self) -> None:
        """
        Creates a "students" table in the database if it does not exist already.
        Fields include ID of type int, name of type str, age of type int,
        gender of type str, and grade of type int.
        :return: None
        >>> processor = StudentDatabaseProcessor("students.db")
        >>> processor.create_student_table()
        """
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            grade INTEGER
        );
        """
        with self._get_connection() as conn:
            conn.execute(create_table_sql)
            conn.commit()

    def insert_student(self, student_data: Dict[str, any]) -> None:
        """
        Inserts a new student into the "students" table.
        :param student_data: dict, a dictionary containing the student's information
                             (name, age, gender, grade).
        :return: None
        >>> processor = StudentDatabaseProcessor("students.db")
        >>> processor.create_student_table()
        >>> student_data = {'name': 'John', 'age': 15, 'gender': 'Male', 'grade': 9}
        >>> processor.insert_student(student_data)
        """
        insert_sql = """
        INSERT INTO students (name, age, gender, grade)
        VALUES (:name, :age, :gender, :grade);
        """
        with self._get_connection() as conn:
            conn.execute(insert_sql, student_data)
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
        search_sql = """
        SELECT id, name, age, gender, grade
        FROM students
        WHERE name = ?;
        """
        with self._get_connection() as conn:
            cursor = conn.execute(search_sql, (name,))
            return cursor.fetchall()

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
        delete_sql = """
        DELETE FROM students
        WHERE name = ?;
        """
        with self._get_connection() as conn:
            conn.execute(delete_sql, (name,))
            conn.commit()
