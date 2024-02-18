"""
Contains unit tests for the Toll API endpoints.

This module provides tests for the entry and exit endpoints of the Toll API.
"""

import json
from django.test import Client, TestCase


class TestTollAPI(TestCase):
    """
    Test cases for the Toll API endpoints.
    """

    def setUp(self):
        """
        Set up the test environment.
        """
        self.client = Client()

    def test_entry_endpoint(self):
        """
        Test the /toll/entry endpoint for valid and invalid requests.
        """
        # Test valid entry request
        valid_entry_request = {
            "interchange": "Bahria Interchange",
            "number_plate": "ABC123",
            "entry_time": "2024-02-18T07:34:02.324590",
        }
        response = self.client.post(
            "/toll/entry",
            data=json.dumps(valid_entry_request),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

        # Test invalid entry request with missing fields
        invalid_entry_request = {
            "interchange": "Bahria Interchange",
            "entry_time": "2024-02-18T07:34:02.324590",
        }
        response = self.client.post(
            "/toll/entry",
            data=json.dumps(invalid_entry_request),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_exit_endpoint(self):
        """
        Test the /toll/exit endpoint for valid and invalid requests.
        """
        # Test valid exit request
        valid_entry_request = {
            "interchange": "Bahria Interchange",
            "number_plate": "ABC123",
            "entry_time": "2024-02-18T07:34:02.324590",
        }
        response = self.client.post(
            "/toll/entry",
            data=json.dumps(valid_entry_request),
            content_type="application/json",
        )
        valid_exit_request = {
            "interchange": "Bahria Interchange",
            "number_plate": "ABC123",
            "exit_time": "2024-02-18T12:45:00.000000",
        }
        response = self.client.post(
            "/toll/exit",
            data=json.dumps(valid_exit_request),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        # Test invalid exit request with missing fields
        valid_entry_request = {
            "interchange": "Bahria Interchange",
            "number_plate": "ABC123",
            "entry_time": "2024-02-18T07:34:02.324590",
        }
        response = self.client.post(
            "/toll/entry",
            data=json.dumps(valid_entry_request),
            content_type="application/json",
        )
        invalid_exit_request = {
            "interchange": "Bahria Interchange",
            "exit_time": "2024-02-18T12:45:00.000000",
        }
        response = self.client.post(
            "/toll/exit",
            data=json.dumps(invalid_exit_request),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)

    def test_validation(self):
        """
        Test validation of datetime formats for entry and exit requests.
        """
        # Test entry with invalid date format
        invalid_date_entry_request = {
            "interchange": "Bahria Interchange",
            "number_plate": "ABC123",
            "entry_time": "2024-02-18 07:34:02",
        }
        response = self.client.post(
            "/toll/entry",
            data=json.dumps(invalid_date_entry_request),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        # Test exit with invalid date format
        invalid_date_exit_request = {
            "interchange": "Bahria Interchange",
            "number_plate": "ABC123",
            "exit_time": "2024-02-18 12:45:00",
        }
        response = self.client.post(
            "/toll/exit",
            data=json.dumps(invalid_date_exit_request),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_holiday_discount(self):
        """
        Test holiday discount for entry and exit requests.
        """
        # Test entry on a national holiday
        holiday_entry_request = {
            "interchange": "Bahria Interchange",
            "number_plate": "ABC123",
            "entry_time": "2024-03-23T07:34:02.324590",  # 23rd March (national holiday)
        }
        response = self.client.post(
            "/toll/entry",
            data=json.dumps(holiday_entry_request),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

        # Test exit on a national holiday
        holiday_exit_request = {
            "interchange": "Bahria Interchange",
            "number_plate": "ABC123",
            "exit_time": "2024-03-23T12:45:00.000000",  # 23rd March (national holiday)
        }
        response = self.client.post(
            "/toll/exit",
            data=json.dumps(holiday_exit_request),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertLess(response.json()["Total"], 30)

    def test_even_discount(self):
        """
        Test even number plate discount for entry and exit requests.
        """
        # Test entry on a Monday with an even number plate
        even_entry_request = {
            "interchange": "Ph4 Interchange",
            "number_plate": "ABC122",
            "entry_time": "2024-02-19T07:34:02.324590",  # Monday
        }
        response = self.client.post(
            "/toll/entry",
            data=json.dumps(even_entry_request),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

        # Test exit on a Monday with an even number plate
        even_exit_request = {
            "interchange": "Bahria Interchange",
            "number_plate": "ABC122",
            "exit_time": "2024-02-19T12:45:00.000000",  # Monday
        }
        response = self.client.post(
            "/toll/exit",
            data=json.dumps(even_exit_request),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertLess(response.json()["Total"], 30)

    def test_odd_discount(self):
        """
        Test odd number plate discount for entry and exit requests.
        """
        # Test entry on a Tuesday with an odd number plate
        odd_entry_request = {
            "interchange": "Ph4 Interchange",
            "number_plate": "ABC123",
            "entry_time": "2024-02-20T07:34:02.324590",  # Tuesday
        }
        response = self.client.post(
            "/toll/entry",
            data=json.dumps(odd_entry_request),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

        # Test exit on a Tuesday with an odd number plate
        odd_exit_request = {
            "interchange": "Bahria Interchange",
            "number_plate": "ABC123",
            "exit_time": "2024-02-20T12:45:00.000000",  # Tuesday
        }
        response = self.client.post(
            "/toll/exit",
            data=json.dumps(odd_exit_request),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertLess(response.json()["Total"], 30)
