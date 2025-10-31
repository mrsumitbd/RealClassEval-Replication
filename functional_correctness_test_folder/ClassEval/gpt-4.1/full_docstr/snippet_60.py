
import numpy as np
from datetime import datetime


class MovieBookingSystem:
    """
    this is a class as movie booking system, which allows to add movies, book tickets and check the available movies within a given time range. 
    """

    def __init__(self):
        """
        Initialize movies contains the information about movies
        """
        self.movies = []

    def add_movie(self, name, price, start_time, end_time, n):
        """
        Add a new movie into self.movies
        """
        st = datetime.strptime(start_time, "%H:%M")
        et = datetime.strptime(end_time, "%H:%M")
        movie = {
            'name': name,
            'price': price,
            'start_time': st,
            'end_time': et,
            'seats': np.zeros((n, n))
        }
        self.movies.append(movie)

    def book_ticket(self, name, seats_to_book):
        """
        Book tickets for a movie. Change the seats value in self.movies if book successfully.
        """
        for movie in self.movies:
            if movie['name'] == name:
                seats = movie['seats']
                # Check if all seats are available
                can_book = True
                for row, col in seats_to_book:
                    if row < 0 or row >= seats.shape[0] or col < 0 or col >= seats.shape[1]:
                        can_book = False
                        break
                    if seats[row, col] != 0:
                        can_book = False
                        break
                if not can_book:
                    return "Booking failed."
                # Book the seats
                for row, col in seats_to_book:
                    seats[row, col] = 1
                return "Booking success."
        return "Movie not found."

    def available_movies(self, start_time, end_time):
        """
        Get a list of available movies within the specified time range
        """
        st = datetime.strptime(start_time, "%H:%M")
        et = datetime.strptime(end_time, "%H:%M")
        available = []
        for movie in self.movies:
            if movie['start_time'] >= st and movie['end_time'] <= et:
                available.append(movie['name'])
        return available
