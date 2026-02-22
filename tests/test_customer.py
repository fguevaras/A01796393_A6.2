"""Unit tests for the Customer class."""

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), '..', 'source')
)

# pylint: disable=wrong-import-position
from customer import Customer  # noqa: E402
# pylint: enable=wrong-import-position


class TestCustomer(unittest.TestCase):
    """Test cases for the Customer class."""

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
    # create_customer                                                    #
    # ------------------------------------------------------------------ #
    def test_create_customer_success(self):
        """Create a customer and verify its attributes."""
        customer = Customer.create_customer(
            'C001', 'Juan Perez', 'juan@example.com', '555-1234',
            file_path=self.file_path
        )
        self.assertIsNotNone(customer)
        self.assertEqual(customer.customer_id, 'C001')
        self.assertEqual(customer.name, 'Juan Perez')
        self.assertEqual(customer.email, 'juan@example.com')
        self.assertEqual(customer.phone, '555-1234')

    def test_create_customer_persisted(self):
        """Created customer is saved and retrievable from file."""
        Customer.create_customer(
            'C001', 'Juan Perez', 'juan@example.com', '555-1234',
            file_path=self.file_path
        )
        customers = Customer.load_customers(self.file_path)
        self.assertIn('C001', customers)

    def test_create_customer_duplicate_returns_none(self):
        """Creating a customer with an existing ID returns None."""
        Customer.create_customer(
            'C001', 'Juan Perez', 'juan@example.com', '555-1234',
            file_path=self.file_path
        )
        result = Customer.create_customer(
            'C001', 'Maria Lopez', 'maria@example.com', '555-5678',
            file_path=self.file_path
        )
        self.assertIsNone(result)

    # ------------------------------------------------------------------ #
    # delete_customer                                                    #
    # ------------------------------------------------------------------ #
    def test_delete_customer_success(self):
        """Delete an existing customer returns True and removes it."""
        Customer.create_customer(
            'C001', 'Juan Perez', 'juan@example.com', '555-1234',
            file_path=self.file_path
        )
        result = Customer.delete_customer('C001', file_path=self.file_path)
        self.assertTrue(result)
        customers = Customer.load_customers(self.file_path)
        self.assertNotIn('C001', customers)

    def test_delete_customer_not_found_returns_false(self):
        """Deleting a non-existent customer returns False."""
        result = Customer.delete_customer(
            'INVALID', file_path=self.file_path
        )
        self.assertFalse(result)

    # ------------------------------------------------------------------ #
    # display_customer_info                                              #
    # ------------------------------------------------------------------ #
    def test_display_customer_info_success(self):
        """Display info for an existing customer returns Customer instance."""
        Customer.create_customer(
            'C001', 'Juan Perez', 'juan@example.com', '555-1234',
            file_path=self.file_path
        )
        customer = Customer.display_customer_info(
            'C001', file_path=self.file_path
        )
        self.assertIsNotNone(customer)
        self.assertEqual(customer.customer_id, 'C001')

    def test_display_customer_info_not_found_returns_none(self):
        """Display info for a non-existent customer returns None."""
        result = Customer.display_customer_info(
            'INVALID', file_path=self.file_path
        )
        self.assertIsNone(result)

    # ------------------------------------------------------------------ #
    # modify_customer                                                    #
    # ------------------------------------------------------------------ #
    def test_modify_customer_success(self):
        """Modify customer email successfully."""
        Customer.create_customer(
            'C001', 'Juan Perez', 'juan@example.com', '555-1234',
            file_path=self.file_path
        )
        result = Customer.modify_customer(
            'C001', file_path=self.file_path, email='nuevo@example.com'
        )
        self.assertTrue(result)
        customers = Customer.load_customers(self.file_path)
        self.assertEqual(customers['C001'].email, 'nuevo@example.com')

    def test_modify_customer_not_found_returns_false(self):
        """Modifying a non-existent customer returns False."""
        result = Customer.modify_customer(
            'INVALID', file_path=self.file_path, name='New Name'
        )
        self.assertFalse(result)

    def test_modify_customer_invalid_field_is_skipped(self):
        """Modifying with an invalid field is skipped, returns True."""
        Customer.create_customer(
            'C001', 'Juan Perez', 'juan@example.com', '555-1234',
            file_path=self.file_path
        )
        result = Customer.modify_customer(
            'C001', file_path=self.file_path, invalid_field='value'
        )
        self.assertTrue(result)

    # ------------------------------------------------------------------ #
    # Helper methods                                                     #
    # ------------------------------------------------------------------ #
    def test_to_dict(self):
        """to_dict returns the correct dictionary representation."""
        customer = Customer(
            'C001', 'Juan Perez', 'juan@example.com', '555-1234'
        )
        data = customer.to_dict()
        self.assertEqual(data['customer_id'], 'C001')
        self.assertEqual(data['name'], 'Juan Perez')
        self.assertEqual(data['email'], 'juan@example.com')
        self.assertEqual(data['phone'], '555-1234')

    def test_from_dict(self):
        """from_dict creates a Customer instance with correct attributes."""
        data = {
            'customer_id': 'C001',
            'name': 'Juan Perez',
            'email': 'juan@example.com',
            'phone': '555-1234',
        }
        customer = Customer.from_dict(data)
        self.assertEqual(customer.customer_id, 'C001')
        self.assertEqual(customer.name, 'Juan Perez')
        self.assertEqual(customer.email, 'juan@example.com')
        self.assertEqual(customer.phone, '555-1234')

    def test_load_customers_nonexistent_file(self):
        """Loading from a non-existent file returns empty dict."""
        customers = Customer.load_customers('/nonexistent/path/customers.json')
        self.assertEqual(customers, {})

    def test_load_customers_invalid_json(self):
        """Loading from a file with invalid JSON returns empty dict."""
        with open(self.file_path, 'w', encoding='utf-8') as file:
            file.write('{ invalid json :::')
        customers = Customer.load_customers(self.file_path)
        self.assertEqual(customers, {})

    def test_load_customers_missing_keys(self):
        """Loading from a file with missing keys returns empty dict."""
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump({'C001': {'customer_id': 'C001'}}, file)
        customers = Customer.load_customers(self.file_path)
        self.assertEqual(customers, {})


if __name__ == '__main__':
    unittest.main()
