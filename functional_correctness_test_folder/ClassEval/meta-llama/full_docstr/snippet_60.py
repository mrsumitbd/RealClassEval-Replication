
import datetime
import numpy as np


class MovieBookingSystem:
    """
    this is a class as movie booking system, which allows to add movies, book tickets and check the available movies within a given time range. 
    """

    def __init__(self):
        """
        Initialize movies contains the information about movies
        >>> system.movies
        [{'name': 'Batman', 'price': 49.9, 'start_time': datetime.datetime(1900, 1, 1, 17, 5), 'end_time': datetime.datetime(1900, 1, 1, 19, 25),
        'seats': array([[0., 0., 0.],
            [0., 0., 0.],
            [0., 0., 0.]])}]
        """
        self.movies = []

    def add_movie(self, name, price, start_time, end_time, n):
        """
        Add a new movie into self.movies
        :param name: str, movie name
        :param price: float, price for one ticket
        :param start_time: str
        :param end_time: str
        :param n: int, the size of seats(n*n)
        >>> system.add_movie('Batman', 49.9, '17:05', '19:25', 3)
        >>> system.movies
        [{'name': 'Batman', 'price': 49.9, 'start_time': datetime.datetime(1900, 1, 1, 17, 5), 'end_time': datetime.datetime(1900, 1, 1, 19, 25),
        'seats': array([[0., 0., 0.],
            [0., 0., 0.],
            [0., 0., 0.]])}]
        """
        start_hour, start_minute = map(int, start_time.split(':'))
        end_hour, end_minute = map(int, end_time.split(':'))
        movie = {
            'name': name,
            'price': price,
            'start_time': datetime.datetime(1900, 1, 1, start_hour, start_minute),
            'end_time': datetime.datetime(1900, 1, 1, end_hour, end_minute),
            'seats': np.zeros((n, n))
        }
        self.movies.append(movie)

    def book_ticket(self, name, seats_to_book):
        """
        Book tickets for a movie. Change the seats value in self.movies if book successfully.
        :param name: str, movie name
        :param seats_to_book: list of tuples, representing seats to book [(row1, col1), (row2, col2), ...]
        :return: str, booking status message. "Movie not found." for no such movie.
                "Booking success." for successfully booking, or "Booking failed." otherwise
        >>> system.add_movie('Batman', 49.9, '17:05', '19:25', 3)
        >>> system.book_ticket('Batman', [(0, 0), (0, 1)])
        'Booking success.'
        >>> system.book_ticket('Batman', [(0, 0)])
        'Booking failed.'
        >>> system.book_ticket('batman', [(0, 0)])
        'Movie not found.'
        """
        for movie in self.movies:
            if movie['name'] == name:
                n = movie['seats'].shape[0]
                for row, col in seats_to_book:
                    if row < 0 or row >= n or col < 0 or col >= n or movie['seats'][row, col] == 1:
                        return 'Booking failed.'
                for row, col in seats_to_book:
                    movie['seats'][row, col] = 1
                return 'Booking success.'
        return 'Movie not found.'

    def available_movies(self, start_time, end_time):
        """
        Get a list of available movies within the specified time range
        :param start_time: str, start time in HH:MM format
        :param end_time: str, end time in HH:MM format
        :return: list of str, names of available movies
        >>> system.add_movie('Batman', 49.9, '17:05', '19:25', 3)
        >>> system.available_movies('12:00', '22:00')
        ['Batman']
        """
        start_hour, start_minute = map(int, start_time.split(':'))
        end_hour, end_minute = map(int, end_time.split(':'))
        start = datetime.datetime(1900, 1, 1, start_hour, start_minute)
        end = datetime.datetime(1900, 1, 1, end_hour, end_minute)
        available_movies = [movie['name'] for movie in self.movies
                            if start <= movie['start_time'] and movie['end_time'] <= end]
        return available_movies


# Example usage:
if __name__ == "__main__":
    system = MovieBookingSystem()
    system.add_movie('Batman', 49.9, '17:05', '19:25', 3)
    print(system.book_ticket('Batman', [(0, 0), (0, 1)]))  # Booking success.
    print(system.book_ticket('Batman', [(0, 0)]))  # Booking failed.
    print(system.book_ticket('batman', [(0, 0)]))  # Movie not found.
    print(system.available_movies('12:00', '22:00'))  # ['Batman']
