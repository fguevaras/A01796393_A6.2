"""Customer module for the Reservation System."""

import json
import os


class Customer:
    """Represents a customer in the reservation system."""

    DEFAULT_FILE = "customers.json"

    def __init__(self, customer_id, name, email, phone):
        """Initialize a Customer instance."""
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone

    # ------------------------------------------------------------------ #
    # a. Create Customer                                                 #
    # ------------------------------------------------------------------ #
    @staticmethod
    def create_customer(customer_id, name, email, phone, file_path=None):
        """Create a new customer and persist it to the file.

        Returns the Customer instance or None if it already exists.
        """
        file_path = file_path or Customer.DEFAULT_FILE
        customers = Customer.load_customers(file_path)
        if customer_id in customers:
            print(f"Customer with ID '{customer_id}' already exists.")
            return None
        customer = Customer(customer_id, name, email, phone)
        customers[customer_id] = customer
        Customer.save_customers(customers, file_path)
        return customer

    # ------------------------------------------------------------------ #
    # b. Delete a Customer                                               #
    # ------------------------------------------------------------------ #
    @staticmethod
    def delete_customer(customer_id, file_path=None):
        """Delete a customer by ID from the file.

        Returns True on success, False if not found.
        """
        file_path = file_path or Customer.DEFAULT_FILE
        customers = Customer.load_customers(file_path)
        if customer_id not in customers:
            print(f"Customer with ID '{customer_id}' not found.")
            return False
        del customers[customer_id]
        Customer.save_customers(customers, file_path)
        return True

    # ------------------------------------------------------------------ #
    # c. Display Customer Information                                    #
    # ------------------------------------------------------------------ #
    @staticmethod
    def display_customer_info(customer_id, file_path=None):
        """Display information for a specific customer.

        Returns the Customer instance or None if not found.
        """
        file_path = file_path or Customer.DEFAULT_FILE
        customers = Customer.load_customers(file_path)
        if customer_id not in customers:
            print(f"Customer with ID '{customer_id}' not found.")
            return None
        customer = customers[customer_id]
        print(f"Customer ID: {customer.customer_id}")
        print(f"Name:        {customer.name}")
        print(f"Email:       {customer.email}")
        print(f"Phone:       {customer.phone}")
        return customer

    # ------------------------------------------------------------------ #
    # d. Modify Customer Information                                     #
    # ------------------------------------------------------------------ #
    @staticmethod
    def modify_customer(customer_id, file_path=None, **kwargs):
        """Modify customer attributes by customer_id.

        Accepted kwargs: name, email, phone.
        Returns True on success, False if not found.
        """
        file_path = file_path or Customer.DEFAULT_FILE
        customers = Customer.load_customers(file_path)
        if customer_id not in customers:
            print(f"Customer with ID '{customer_id}' not found.")
            return False
        customer = customers[customer_id]
        valid_fields = {"name", "email", "phone"}
        for key, value in kwargs.items():
            if key in valid_fields:
                setattr(customer, key, value)
            else:
                print(f"Invalid field '{key}' — skipped.")
        Customer.save_customers(customers, file_path)
        return True

    # ------------------------------------------------------------------ #
    # Helper methods                                                     #
    # ------------------------------------------------------------------ #
    def to_dict(self):
        """Convert the Customer instance to a dictionary."""
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Customer instance from a dictionary."""
        return cls(
            data["customer_id"],
            data["name"],
            data["email"],
            data["phone"],
        )

    @staticmethod
    def load_customers(file_path=None):
        """Load customers from a JSON file.

        Returns an empty dict if the file does not exist or is invalid.
        """
        file_path = file_path or Customer.DEFAULT_FILE
        if not os.path.exists(file_path):
            return {}
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            return {k: Customer.from_dict(v) for k, v in data.items()}
        except (json.JSONDecodeError, KeyError, TypeError) as err:
            print(f"Error loading customers file: {err}")
            return {}

    @staticmethod
    def save_customers(customers, file_path=None):
        """Save customers dictionary to a JSON file."""
        file_path = file_path or Customer.DEFAULT_FILE
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(
                    {k: v.to_dict() for k, v in customers.items()},
                    file,
                    indent=4,
                )
        except IOError as err:
            print(f"Error saving customers file: {err}")
