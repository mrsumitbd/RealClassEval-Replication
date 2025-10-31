
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
        self.available_rooms = rooms
        self.booked_rooms = {}

    def book_room(self, room_type, room_number, name):
        """
        Check if there are any rooms of the specified type available.
        if rooms are adequate, modify available_rooms and booked_rooms and finish booking, or fail to book otherwise.
        """
        if room_type not in self.available_rooms:
            return False
        if self.available_rooms[room_type] == 0:
            return False
        if room_number > self.available_rooms[room_type]:
            return self.available_rooms[room_type]
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
        Check if the room of the specified type and number is booked by the person named name.
        Remove this name when check in successfuly(room_number is equal to specific person's booked_rooms. When the actual check in quantity (room_number) is less than the booked quantity, number in booked_rooms will be booked quantity minus actual quantity
        """
        if room_type not in self.booked_rooms or name not in self.booked_rooms[room_type]:
            return False
        if room_number > self.booked_rooms[room_type][name]:
            return False
        self.booked_rooms[room_type][name] -= room_number
        if self.booked_rooms[room_type][name] == 0:
            del self.booked_rooms[room_type][name]
        if not self.booked_rooms[room_type]:
            del self.booked_rooms[room_type]

    def check_out(self, room_type, room_number):
        """
        Check out rooms, add number for specific type in available_rooms.
        If room_type is new, add new type in available_rooms.
        """
        if room_type in self.available_rooms:
            self.available_rooms[room_type] += room_number
        else:
            self.available_rooms[room_type] = room_number

    def get_available_rooms(self, room_type):
        """
        Get the number of specific type of available rooms.
        """
        return self.available_rooms.get(room_type, 0)
