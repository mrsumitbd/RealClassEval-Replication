
class Hotel:
    """
    This is a class as hotel management system, managing the booking, check-in, check-out, and availability of rooms in a hotel with different room types.
    """

    def __init__(self, name, rooms):
        """
        Initialize the three fields in Hotel System.
        name is the hotel name.
        available_rooms stores the remaining rooms in the hotel
        booked_rooms stores the rooms that have been booked and the person's name who booked rooms.
        """
        self.name = name
        self.available_rooms = dict(rooms)
        self.booked_rooms = {k: {} for k in rooms}

    def book_room(self, room_type, room_number, name):
        """
        Book rooms if available.
        """
        if room_type not in self.available_rooms:
            return False
        available = self.available_rooms[room_type]
        if available == 0:
            return False
        if room_number > available:
            return available
        # Book the room
        self.available_rooms[room_type] -= room_number
        if room_type not in self.booked_rooms:
            self.booked_rooms[room_type] = {}
        if name in self.booked_rooms[room_type]:
            self.booked_rooms[room_type][name] += room_number
        else:
            self.booked_rooms[room_type][name] = room_number
        return 'Success!'

    def check_in(self, room_type, room_number, name):
        """
        Check in booked rooms.
        """
        if room_type not in self.booked_rooms:
            return False
        if name not in self.booked_rooms[room_type]:
            return False
        booked = self.booked_rooms[room_type][name]
        if room_number > booked:
            return False
        if room_number == booked:
            del self.booked_rooms[room_type][name]
        else:
            self.booked_rooms[room_type][name] -= room_number

    def check_out(self, room_type, room_number):
        """
        Check out rooms, add number for specific type in available_rooms.
        """
        if room_type in self.available_rooms:
            self.available_rooms[room_type] += room_number
        else:
            self.available_rooms[room_type] = room_number
        if room_type not in self.booked_rooms:
            self.booked_rooms[room_type] = {}

    def get_available_rooms(self, room_type):
        """
        Get the number of specific type of available rooms.
        """
        return self.available_rooms.get(room_type, 0)
