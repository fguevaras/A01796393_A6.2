"""Reservation module for the Reservation System."""

import json
import os


class Reservation:
    """Represents a reservation linking a customer and a hotel."""

    DEFAULT_FILE = "reservations.json"

    def __init__(self, reservation_id, customer_id, hotel_id):
        """Initialize a Reservation instance."""
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.hotel_id = hotel_id

    # ------------------------------------------------------------------ #
    # a. Create a Reservation (Customer, Hotel)                          #
    # ------------------------------------------------------------------ #
    @staticmethod
    def create_reservation(
        reservation_id, customer_id, hotel_id, file_path=None
    ):
        """Create a new reservation and persist it to the file.

        Returns the Reservation instance or None if it already exists.
        """
        file_path = file_path or Reservation.DEFAULT_FILE
        reservations = Reservation.load_reservations(file_path)
        if reservation_id in reservations:
            print(
                f"Reservation with ID '{reservation_id}' already exists."
            )
            return None
        reservation = Reservation(reservation_id, customer_id, hotel_id)
        reservations[reservation_id] = reservation
        Reservation.save_reservations(reservations, file_path)
        return reservation

    # ------------------------------------------------------------------ #
    # b. Cancel a Reservation                                            #
    # ------------------------------------------------------------------ #
    @staticmethod
    def cancel_reservation(reservation_id, file_path=None):
        """Cancel (delete) a reservation by ID from the file.

        Returns True on success, False if not found.
        """
        file_path = file_path or Reservation.DEFAULT_FILE
        reservations = Reservation.load_reservations(file_path)
        if reservation_id not in reservations:
            print(f"Reservation with ID '{reservation_id}' not found.")
            return False
        del reservations[reservation_id]
        Reservation.save_reservations(reservations, file_path)
        return True

    # ------------------------------------------------------------------ #
    # Helper methods                                                     #
    # ------------------------------------------------------------------ #
    def to_dict(self):
        """Convert the Reservation instance to a dictionary."""
        return {
            "reservation_id": self.reservation_id,
            "customer_id": self.customer_id,
            "hotel_id": self.hotel_id,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Reservation instance from a dictionary."""
        return cls(
            data["reservation_id"],
            data["customer_id"],
            data["hotel_id"],
        )

    @staticmethod
    def load_reservations(file_path=None):
        """Load reservations from a JSON file.

        Returns an empty dict if the file does not exist or is invalid.
        """
        file_path = file_path or Reservation.DEFAULT_FILE
        if not os.path.exists(file_path):
            return {}
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            return {
                k: Reservation.from_dict(v) for k, v in data.items()
            }
        except (json.JSONDecodeError, KeyError, TypeError) as err:
            print(f"Error loading reservations file: {err}")
            return {}

    @staticmethod
    def save_reservations(reservations, file_path=None):
        """Save reservations dictionary to a JSON file."""
        file_path = file_path or Reservation.DEFAULT_FILE
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(
                    {k: v.to_dict() for k, v in reservations.items()},
                    file,
                    indent=4,
                )
        except IOError as err:
            print(f"Error saving reservations file: {err}")
