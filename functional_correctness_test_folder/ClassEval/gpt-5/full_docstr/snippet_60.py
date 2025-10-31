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
        st = datetime.datetime.strptime(start_time, "%H:%M")
        et = datetime.datetime.strptime(end_time, "%H:%M")
        seats = np.zeros((n, n), dtype=float)
        self.movies.append({
            'name': name,
            'price': float(price),
            'start_time': st,
            'end_time': et,
            'seats': seats
        })

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
        movie = None
        for m in self.movies:
            if m['name'] == name:
                movie = m
                break
        if movie is None:
            return "Movie not found."
        seats = movie['seats']
        nrows, ncols = seats.shape
        # Validate all seats
        for r, c in seats_to_book:
            if not (isinstance(r, int) and isinstance(c, int)):
                return "Booking failed."
            if r < 0 or c < 0 or r >= nrows or c >= ncols:
                return "Booking failed."
            if seats[r, c] != 0.0:
                return "Booking failed."
        # Book seats
        for r, c in seats_to_book:
            seats[r, c] = 1.0
        return "Booking success."

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
        st = datetime.datetime.strptime(start_time, "%H:%M")
        et = datetime.datetime.strptime(end_time, "%H:%M")
        result = []
        for m in self.movies:
            if m['start_time'] >= st and m['end_time'] <= et:
                result.append(m['name'])
        return result
