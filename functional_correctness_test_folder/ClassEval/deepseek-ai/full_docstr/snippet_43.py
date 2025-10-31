
class Hotel:
    """
    This is a class as hotel management system, managing the booking, check-in, check-out, and availability of rooms in a hotel with different room types.
    """

    def __init__(self, name, rooms):
        self.name = name
        self.available_rooms = rooms
        self.booked_rooms = {}

    def book_room(self, room_type, room_number, name):
        if room_type not in self.available_rooms or self.available_rooms[room_type] == 0:
            return False
        available = self.available_rooms[room_type]
        if room_number <= available:
            self.available_rooms[room_type] -= room_number
            if room_type not in self.booked_rooms:
                self.booked_rooms[room_type] = {}
            if name not in self.booked_rooms[room_type]:
                self.booked_rooms[room_type][name] = 0
            self.booked_rooms[room_type][name] += room_number
            return 'Success!'
        else:
            return available

    def check_in(self, room_type, room_number, name):
        if room_type not in self.booked_rooms:
            return False
        if name not in self.booked_rooms[room_type]:
            return False
        booked = self.booked_rooms[room_type][name]
        if room_number > booked:
            return False
        if room_number == booked:
            del self.booked_rooms[room_type][name]
            if not self.booked_rooms[room_type]:
                del self.booked_rooms[room_type]
        else:
            self.booked_rooms[room_type][name] -= room_number

    def check_out(self, room_type, room_number):
        if room_type in self.available_rooms:
            self.available_rooms[room_type] += room_number
        else:
            self.available_rooms[room_type] = room_number

    def get_available_rooms(self, room_type):
        return self.available_rooms.get(room_type, 0)
