"""Unit tests for the Hotel class."""

import json
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), '..', 'source')
)

from hotel import Hotel  # noqa: E402  # pylint: disable=wrong-import-position

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


class TestHotel(unittest.TestCase):
    """Test cases for the Hotel class."""

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
    # Create Hotel                                                       #
    # ------------------------------------------------------------------ #
    def test_create_hotel_success(self):
        """Create a hotel and verify its attributes."""
        hotel = Hotel.create_hotel(
            'H001', 'Hotel Riviera Maya', 'Playa del Carmen', 100,
            file_path=self.file_path
        )
        self.assertIsNotNone(hotel)
        self.assertEqual(hotel.hotel_id, 'H001')
        self.assertEqual(hotel.name, 'Hotel Riviera Maya')
        self.assertEqual(hotel.location, 'Playa del Carmen')
        self.assertEqual(hotel.total_rooms, 100)
        self.assertEqual(hotel.available_rooms, 100)

    def test_create_hotel_persisted(self):
        """Created hotel is saved and retrievable from file."""
        Hotel.create_hotel(
            'H001', 'Hotel Riviera Maya', 'Playa del Carmen', 100,
            file_path=self.file_path
        )
        hotels = Hotel.load_hotels(self.file_path)
        self.assertIn('H001', hotels)

    def test_create_hotel_duplicate_returns_none(self):
        """Creating a hotel with an existing ID returns None."""
        Hotel.create_hotel(
            'H001', 'Hotel Riviera Maya', 'Playa del Carmen', 100,
            file_path=self.file_path
        )
        result = Hotel.create_hotel(
            'H001', 'Other Hotel', 'Guadalajara', 50,
            file_path=self.file_path
        )
        self.assertIsNone(result)

    # ------------------------------------------------------------------ #
    # Delete Hotel                                                       #
    # ------------------------------------------------------------------ #
    def test_delete_hotel_success(self):
        """Delete an existing hotel returns True and removes it."""
        Hotel.create_hotel(
            'H001', 'Hotel Riviera Maya', 'Playa del Carmen', 100,
            file_path=self.file_path
        )
        result = Hotel.delete_hotel('H001', file_path=self.file_path)
        self.assertTrue(result)
        hotels = Hotel.load_hotels(self.file_path)
        self.assertNotIn('H001', hotels)

    def test_delete_hotel_not_found_returns_false(self):
        """Deleting a non-existent hotel returns False."""
        result = Hotel.delete_hotel('INVALID', file_path=self.file_path)
        self.assertFalse(result)

    # ------------------------------------------------------------------ #
    # Display Hotel information                                          #
    # ------------------------------------------------------------------ #
    def test_display_hotel_info_success(self):
        """Display info for an existing hotel returns Hotel instance."""
        Hotel.create_hotel(
            'H001', 'Hotel Riviera Maya', 'Playa del Carmen', 100,
            file_path=self.file_path
        )
        hotel = Hotel.display_hotel_info(
            'H001', file_path=self.file_path
        )
        self.assertIsNotNone(hotel)
        self.assertEqual(hotel.hotel_id, 'H001')

    def test_display_hotel_info_not_found_returns_none(self):
        """Display info for a non-existent hotel returns None."""
        result = Hotel.display_hotel_info(
            'INVALID', file_path=self.file_path
        )
        self.assertIsNone(result)

    # ------------------------------------------------------------------ #
    # Modify Hotel Information                                           #
    # ------------------------------------------------------------------ #
    def test_modify_hotel_success(self):
        """Modify hotel name successfully."""
        Hotel.create_hotel(
            'H001', 'Hotel Riviera Maya', 'Playa del Carmen', 100,
            file_path=self.file_path
        )
        result = Hotel.modify_hotel(
            'H001', file_path=self.file_path, name='New Name'
        )
        self.assertTrue(result)
        hotels = Hotel.load_hotels(self.file_path)
        self.assertEqual(hotels['H001'].name, 'New Name')

    def test_modify_hotel_not_found_returns_false(self):
        """Modifying a non-existent hotel returns False."""
        result = Hotel.modify_hotel(
            'INVALID', file_path=self.file_path, name='New Name'
        )
        self.assertFalse(result)

    def test_modify_hotel_invalid_field_is_skipped(self):
        """Modifying with an invalid field is skipped, returns True."""
        Hotel.create_hotel(
            'H001', 'Hotel Riviera Maya', 'Playa del Carmen', 100,
            file_path=self.file_path
        )
        result = Hotel.modify_hotel(
            'H001', file_path=self.file_path, invalid_field='value'
        )
        self.assertTrue(result)

    # ------------------------------------------------------------------ #
    # Reserve a Room                                                     #
    # ------------------------------------------------------------------ #
    def test_reserve_room_success(self):
        """Reserve a room decrements available_rooms and logs ID."""
        Hotel.create_hotel(
            'H001', 'Hotel Riviera Maya', 'Playa del Carmen', 5,
            file_path=self.file_path
        )
        result = Hotel.reserve_room(
            'H001', 'R001', file_path=self.file_path
        )
        self.assertTrue(result)
        hotels = Hotel.load_hotels(self.file_path)
        self.assertEqual(hotels['H001'].available_rooms, 4)
        self.assertIn('R001', hotels['H001'].reservations)

    def test_reserve_room_hotel_not_found_returns_false(self):
        """Reserve a room in a non-existent hotel returns False."""
        result = Hotel.reserve_room(
            'INVALID', 'R001', file_path=self.file_path
        )
        self.assertFalse(result)

    def test_reserve_room_no_availability_returns_false(self):
        """Reserve a room when fully booked returns False."""
        Hotel.create_hotel(
            'H001', 'Hotel Riviera Maya', 'Playa del Carmen', 1,
            file_path=self.file_path
        )
        Hotel.reserve_room('H001', 'R001', file_path=self.file_path)
        result = Hotel.reserve_room(
            'H001', 'R002', file_path=self.file_path
        )
        self.assertFalse(result)

    def test_reserve_room_duplicate_id_returns_false(self):
        """Reserve a room with a duplicate reservation ID returns False."""
        Hotel.create_hotel(
            'H001', 'Hotel Riviera Maya', 'Playa del Carmen', 5,
            file_path=self.file_path
        )
        Hotel.reserve_room('H001', 'R001', file_path=self.file_path)
        result = Hotel.reserve_room(
            'H001', 'R001', file_path=self.file_path
        )
        self.assertFalse(result)

    # ------------------------------------------------------------------ #
    # Cancel a Reservation                                               #
    # ------------------------------------------------------------------ #
    def test_cancel_reservation_success(self):
        """Cancel a reservation restores available_rooms."""
        Hotel.create_hotel(
            'H001', 'Hotel Riviera Maya', 'Playa del Carmen', 5,
            file_path=self.file_path
        )
        Hotel.reserve_room('H001', 'R001', file_path=self.file_path)
        result = Hotel.cancel_reservation(
            'H001', 'R001', file_path=self.file_path
        )
        self.assertTrue(result)
        hotels = Hotel.load_hotels(self.file_path)
        self.assertEqual(hotels['H001'].available_rooms, 5)
        self.assertNotIn('R001', hotels['H001'].reservations)

    def test_cancel_reservation_hotel_not_found_returns_false(self):
        """Cancel reservation in non-existent hotel returns False."""
        result = Hotel.cancel_reservation(
            'INVALID', 'R001', file_path=self.file_path
        )
        self.assertFalse(result)

    def test_cancel_reservation_not_found_returns_false(self):
        """Cancel a non-existent reservation returns False."""
        Hotel.create_hotel(
            'H001', 'Hotel Riviera Maya', 'Playa del Carmen', 5,
            file_path=self.file_path
        )
        result = Hotel.cancel_reservation(
            'H001', 'INVALID', file_path=self.file_path
        )
        self.assertFalse(result)

    # ------------------------------------------------------------------ #
    # Helper methods                                                     #
    # ------------------------------------------------------------------ #
    def test_to_dict(self):
        """to_dict returns the correct dictionary representation."""
        hotel = Hotel('H001', 'Hotel Riviera Maya', 'Playa del Carmen', 100)
        data = hotel.to_dict()
        self.assertEqual(data['hotel_id'], 'H001')
        self.assertEqual(data['name'], 'Hotel Riviera Maya')
        self.assertEqual(data['location'], 'Playa del Carmen')
        self.assertEqual(data['total_rooms'], 100)
        self.assertEqual(data['available_rooms'], 100)
        self.assertEqual(data['reservations'], [])

    def test_from_dict(self):
        """from_dict creates a Hotel instance with correct attributes."""
        data = {
            'hotel_id': 'H001',
            'name': 'Hotel Riviera Maya',
            'location': 'Playa del Carmen',
            'total_rooms': 100,
            'available_rooms': 80,
            'reservations': ['R001'],
        }
        hotel = Hotel.from_dict(data)
        self.assertEqual(hotel.hotel_id, 'H001')
        self.assertEqual(hotel.available_rooms, 80)
        self.assertIn('R001', hotel.reservations)

    def test_load_hotels_nonexistent_file(self):
        """Loading from a non-existent file returns empty dict."""
        hotels = Hotel.load_hotels('/nonexistent/path/hotels.json')
        self.assertEqual(hotels, {})

    def test_load_hotels_invalid_json(self):
        """Loading from a file with invalid JSON returns empty dict."""
        with open(self.file_path, 'w', encoding='utf-8') as file:
            file.write('{ invalid json :::')
        hotels = Hotel.load_hotels(self.file_path)
        self.assertEqual(hotels, {})

    def test_load_hotels_missing_keys(self):
        """Loading from a file with missing keys returns empty dict."""
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump({'H001': {'hotel_id': 'H001'}}, file)
        hotels = Hotel.load_hotels(self.file_path)
        self.assertEqual(hotels, {})

    # ------------------------------------------------------------------ #
    # Data file tests                                                    #
    # ------------------------------------------------------------------ #

    def test_load_hotels_from_data_file(self):
        """Load hotels from the pre-existing data file."""
        src = os.path.join(DATA_DIR, 'hotels.json')
        hotels = Hotel.load_hotels(src)
        self.assertIn('H001', hotels)
        self.assertIn('H002', hotels)
        self.assertEqual(hotels['H001'].name, 'Hotel Riviera Maya')
        self.assertEqual(hotels['H001'].available_rooms, 98)
        self.assertIn('R001', hotels['H001'].reservations)

    def test_display_hotel_from_data_file(self):
        """Display hotel info loaded from the pre-existing data file."""
        shutil.copy(os.path.join(DATA_DIR, 'hotels.json'), self.file_path)
        hotel = Hotel.display_hotel_info('H002', file_path=self.file_path)
        self.assertIsNotNone(hotel)
        self.assertEqual(hotel.location, 'Nuevo Vallarta')

    def test_create_hotel_duplicate_from_data_file(self):
        """Creating a duplicate hotel ID from data file returns None."""
        shutil.copy(os.path.join(DATA_DIR, 'hotels.json'), self.file_path)
        result = Hotel.create_hotel(
            'H001', 'Duplicate', 'Nowhere', 10,
            file_path=self.file_path
        )
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
