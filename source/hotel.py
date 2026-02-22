"""Hotel module for the Reservation System."""

import json
import os


class Hotel:
    """Represents a hotel in the reservation system."""

    DEFAULT_FILE = "hotels.json"

    def __init__(self, hotel_id, name, location, total_rooms):
        """Initialize a Hotel instance."""
        self.hotel_id = hotel_id
        self.name = name
        self.location = location
        self.total_rooms = total_rooms
        self.available_rooms = total_rooms
        self.reservations = []

    # ------------------------------------------------------------------ #
    # a. Create Hotel                                                    #
    # ------------------------------------------------------------------ #
    @staticmethod
    def create_hotel(hotel_id, name, location, total_rooms, file_path=None):
        """Create a new hotel and persist it to the file.

        Returns the Hotel instance or None if it already exists.
        """
        file_path = file_path or Hotel.DEFAULT_FILE
        hotels = Hotel.load_hotels(file_path)
        if hotel_id in hotels:
            print(f"Hotel with ID '{hotel_id}' already exists.")
            return None
        hotel = Hotel(hotel_id, name, location, total_rooms)
        hotels[hotel_id] = hotel
        Hotel.save_hotels(hotels, file_path)
        return hotel

    # ------------------------------------------------------------------ #
    # b. Delete Hotel                                                    #
    # ------------------------------------------------------------------ #
    @staticmethod
    def delete_hotel(hotel_id, file_path=None):
        """Delete a hotel by ID from the file.

        Returns True on success, False if not found.
        """
        file_path = file_path or Hotel.DEFAULT_FILE
        hotels = Hotel.load_hotels(file_path)
        if hotel_id not in hotels:
            print(f"Hotel with ID '{hotel_id}' not found.")
            return False
        del hotels[hotel_id]
        Hotel.save_hotels(hotels, file_path)
        return True

    # ------------------------------------------------------------------ #
    # c. Display Hotel Information                                       #
    # ------------------------------------------------------------------ #
    @staticmethod
    def display_hotel_info(hotel_id, file_path=None):
        """Display information for a specific hotel.

        Returns the Hotel instance or None if not found.
        """
        file_path = file_path or Hotel.DEFAULT_FILE
        hotels = Hotel.load_hotels(file_path)
        if hotel_id not in hotels:
            print(f"Hotel with ID '{hotel_id}' not found.")
            return None
        hotel = hotels[hotel_id]
        print(f"Hotel ID:        {hotel.hotel_id}")
        print(f"Name:            {hotel.name}")
        print(f"Location:        {hotel.location}")
        print(f"Total Rooms:     {hotel.total_rooms}")
        print(f"Available Rooms: {hotel.available_rooms}")
        print(f"Reservations:    {hotel.reservations}")
        return hotel

    # ------------------------------------------------------------------ #
    # d. Modify Hotel Information                                        #
    # ------------------------------------------------------------------ #
    @staticmethod
    def modify_hotel(hotel_id, file_path=None, **kwargs):
        """Modify hotel attributes by hotel_id.

        Accepted kwargs: name, location, total_rooms.
        Returns True on success, False if not found.
        """
        file_path = file_path or Hotel.DEFAULT_FILE
        hotels = Hotel.load_hotels(file_path)
        if hotel_id not in hotels:
            print(f"Hotel with ID '{hotel_id}' not found.")
            return False
        hotel = hotels[hotel_id]
        valid_fields = {"name", "location", "total_rooms"}
        for key, value in kwargs.items():
            if key in valid_fields:
                setattr(hotel, key, value)
            else:
                print(f"Invalid field '{key}' — skipped.")
        Hotel.save_hotels(hotels, file_path)
        return True

    # ------------------------------------------------------------------ #
    # e. Reserve a Room                                                  #
    # ------------------------------------------------------------------ #
    @staticmethod
    def reserve_room(hotel_id, reservation_id, file_path=None):
        """Reserve a room in a hotel.

        Returns True on success, False otherwise.
        """
        file_path = file_path or Hotel.DEFAULT_FILE
        hotels = Hotel.load_hotels(file_path)
        if hotel_id not in hotels:
            print(f"Hotel with ID '{hotel_id}' not found.")
            return False
        hotel = hotels[hotel_id]
        if hotel.available_rooms <= 0:
            print(f"No available rooms in hotel '{hotel_id}'.")
            return False
        if reservation_id in hotel.reservations:
            print(f"Reservation '{reservation_id}' already exists.")
            return False
        hotel.available_rooms -= 1
        hotel.reservations.append(reservation_id)
        Hotel.save_hotels(hotels, file_path)
        return True

    # ------------------------------------------------------------------ #
    # f. Cancel a Reservation                                            #
    # ------------------------------------------------------------------ #
    @staticmethod
    def cancel_reservation(hotel_id, reservation_id, file_path=None):
        """Cancel a reservation in a hotel.

        Returns True on success, False otherwise.
        """
        file_path = file_path or Hotel.DEFAULT_FILE
        hotels = Hotel.load_hotels(file_path)
        if hotel_id not in hotels:
            print(f"Hotel with ID '{hotel_id}' not found.")
            return False
        hotel = hotels[hotel_id]
        if reservation_id not in hotel.reservations:
            print(
                f"Reservation '{reservation_id}' not found "
                f"in hotel '{hotel_id}'."
            )
            return False
        hotel.reservations.remove(reservation_id)
        hotel.available_rooms += 1
        Hotel.save_hotels(hotels, file_path)
        return True

    # ------------------------------------------------------------------ #
    # Helper methods                                                     #
    # ------------------------------------------------------------------ #
    def to_dict(self):
        """Convert the Hotel instance to a dictionary."""
        return {
            "hotel_id": self.hotel_id,
            "name": self.name,
            "location": self.location,
            "total_rooms": self.total_rooms,
            "available_rooms": self.available_rooms,
            "reservations": self.reservations,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Hotel instance from a dictionary."""
        hotel = cls(
            data["hotel_id"],
            data["name"],
            data["location"],
            data["total_rooms"],
        )
        hotel.available_rooms = data.get(
            "available_rooms", hotel.total_rooms
        )
        hotel.reservations = data.get("reservations", [])
        return hotel

    @staticmethod
    def load_hotels(file_path=None):
        """Load hotels from a JSON file.

        Returns an empty dict if the file does not exist or is invalid.
        """
        file_path = file_path or Hotel.DEFAULT_FILE
        if not os.path.exists(file_path):
            return {}
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            return {k: Hotel.from_dict(v) for k, v in data.items()}
        except (json.JSONDecodeError, KeyError, TypeError) as err:
            print(f"Error loading hotels file: {err}")
            return {}

    @staticmethod
    def save_hotels(hotels, file_path=None):
        """Save hotels dictionary to a JSON file."""
        file_path = file_path or Hotel.DEFAULT_FILE
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(
                    {k: v.to_dict() for k, v in hotels.items()},
                    file,
                    indent=4,
                )
        except IOError as err:
            print(f"Error saving hotels file: {err}")
