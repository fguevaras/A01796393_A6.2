"""Unit tests for the Reservation class."""

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), '..', 'source')
)

# pylint: disable=wrong-import-position
from reservation import Reservation  # noqa: E402
# pylint: enable=wrong-import-position


class TestReservation(unittest.TestCase):
    """Test cases for the Reservation class."""

    def setUp(self):
        """Create a temporary file path for each test."""
        fd, self.file_path = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        os.remove(self.file_path)

    def tearDown(self):
        """Remove the temporary file after each test."""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    # ------------------------------------------------------------------ #
    # Create a Reservation (Customer, Hotel)                             #
    # ------------------------------------------------------------------ #
    def test_create_reservation_success(self):
        """Create a reservation and verify its attributes."""
        reservation = Reservation.create_reservation(
            'R001', 'C001', 'H001', file_path=self.file_path
        )
        self.assertIsNotNone(reservation)
        self.assertEqual(reservation.reservation_id, 'R001')
        self.assertEqual(reservation.customer_id, 'C001')
        self.assertEqual(reservation.hotel_id, 'H001')

    def test_create_reservation_persisted(self):
        """Created reservation is saved and retrievable from file."""
        Reservation.create_reservation(
            'R001', 'C001', 'H001', file_path=self.file_path
        )
        reservations = Reservation.load_reservations(self.file_path)
        self.assertIn('R001', reservations)

    def test_create_reservation_duplicate_returns_none(self):
        """Creating a reservation with an existing ID returns None."""
        Reservation.create_reservation(
            'R001', 'C001', 'H001', file_path=self.file_path
        )
        result = Reservation.create_reservation(
            'R001', 'C002', 'H002', file_path=self.file_path
        )
        self.assertIsNone(result)

    # ------------------------------------------------------------------ #
    # Cancel a Reservation                                               #
    # ------------------------------------------------------------------ #
    def test_cancel_reservation_success(self):
        """Cancel an existing reservation returns True and removes it."""
        Reservation.create_reservation(
            'R001', 'C001', 'H001', file_path=self.file_path
        )
        result = Reservation.cancel_reservation(
            'R001', file_path=self.file_path
        )
        self.assertTrue(result)
        reservations = Reservation.load_reservations(self.file_path)
        self.assertNotIn('R001', reservations)

    def test_cancel_reservation_not_found_returns_false(self):
        """Cancelling a non-existent reservation returns False."""
        result = Reservation.cancel_reservation(
            'INVALID', file_path=self.file_path
        )
        self.assertFalse(result)

    # ------------------------------------------------------------------ #
    # Helper methods                                                     #
    # ------------------------------------------------------------------ #
    def test_to_dict(self):
        """to_dict returns the correct dictionary representation."""
        reservation = Reservation('R001', 'C001', 'H001')
        data = reservation.to_dict()
        self.assertEqual(data['reservation_id'], 'R001')
        self.assertEqual(data['customer_id'], 'C001')
        self.assertEqual(data['hotel_id'], 'H001')

    def test_from_dict(self):
        """from_dict creates a Reservation instance with correct attributes."""
        data = {
            'reservation_id': 'R001',
            'customer_id': 'C001',
            'hotel_id': 'H001',
        }
        reservation = Reservation.from_dict(data)
        self.assertEqual(reservation.reservation_id, 'R001')
        self.assertEqual(reservation.customer_id, 'C001')
        self.assertEqual(reservation.hotel_id, 'H001')

    def test_load_reservations_nonexistent_file(self):
        """Loading from a non-existent file returns empty dict."""
        reservations = Reservation.load_reservations(
            '/nonexistent/path/reservations.json'
        )
        self.assertEqual(reservations, {})

    def test_load_reservations_invalid_json(self):
        """Loading from a file with invalid JSON returns empty dict."""
        with open(self.file_path, 'w', encoding='utf-8') as file:
            file.write('{ invalid json :::')
        reservations = Reservation.load_reservations(self.file_path)
        self.assertEqual(reservations, {})

    def test_load_reservations_missing_keys(self):
        """Loading from a file with missing keys returns empty dict."""
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump({'R001': {'reservation_id': 'R001'}}, file)
        reservations = Reservation.load_reservations(self.file_path)
        self.assertEqual(reservations, {})

    def test_multiple_reservations_persisted(self):
        """Multiple reservations are all saved and retrievable."""
        Reservation.create_reservation(
            'R001', 'C001', 'H001', file_path=self.file_path
        )
        Reservation.create_reservation(
            'R002', 'C002', 'H001', file_path=self.file_path
        )
        reservations = Reservation.load_reservations(self.file_path)
        self.assertIn('R001', reservations)
        self.assertIn('R002', reservations)

    def test_cancel_reservation_leaves_others_intact(self):
        """Cancelling one reservation does not affect others."""
        Reservation.create_reservation(
            'R001', 'C001', 'H001', file_path=self.file_path
        )
        Reservation.create_reservation(
            'R002', 'C002', 'H001', file_path=self.file_path
        )
        Reservation.cancel_reservation('R001', file_path=self.file_path)
        reservations = Reservation.load_reservations(self.file_path)
        self.assertNotIn('R001', reservations)
        self.assertIn('R002', reservations)


if __name__ == '__main__':
    unittest.main()
