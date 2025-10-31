
import datetime
import numpy as np


class MovieBookingSystem:
    def __init__(self):
        self.movies = []

    def add_movie(self, name, price, start_time, end_time, n):
        start = datetime.datetime.strptime(start_time, '%H:%M')
        end = datetime.datetime.strptime(end_time, '%H:%M')
        seats = np.zeros((n, n))
        self.movies.append({
            'name': name,
            'price': price,
            'start_time': start,
            'end_time': end,
            'seats': seats
        })

    def book_ticket(self, name, seats_to_book):
        movie = None
        for m in self.movies:
            if m['name'] == name:
                movie = m
                break
        if not movie:
            return "Movie not found."

        seats = movie['seats']
        for row, col in seats_to_book:
            if row >= seats.shape[0] or col >= seats.shape[1] or seats[row][col] != 0:
                return "Booking failed."

        for row, col in seats_to_book:
            seats[row][col] = 1
        return "Booking success."

    def available_movies(self, start_time, end_time):
        start = datetime.datetime.strptime(start_time, '%H:%M')
        end = datetime.datetime.strptime(end_time, '%H:%M')
        available = []
        for movie in self.movies:
            if not (movie['end_time'] <= start or movie['start_time'] >= end):
                available.append(movie['name'])
        return available
