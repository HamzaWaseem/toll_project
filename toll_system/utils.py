"""
Contains utility functions and constants for the toll system app.

This module provides functions to interact with the database, calculate toll tax,
validate datetime formats, and perform other utility operations.
"""

import datetime
import psycopg2

from toll_system.constants import (
    BASE_TOLL_RATE,
    DISTANCE_RATE,
    HOLIDAY_DISCOUNT,
    NATIONAL_HOLIDAYS,
    SPECIAL_DISCOUNT_DAYS,
    WEEKEND_DISTANCE_RATE_MULTIPLIER,
)


def get_db_connection():
    """
    Establishes a connection to the PostgreSQL database.

    Returns:
    - psycopg2 connection: A connection object to the PostgreSQL database.
    """
    conn = psycopg2.connect(
        dbname="db_test",
        user="root",
        password="admin123",
        host="localhost",
        port="5432",
    )
    return conn


def create_toll_data_table():
    """
    Creates the toll_data table in the database if it doesn't exist.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS toll_data (
            id SERIAL PRIMARY KEY,
            entry_interchange VARCHAR(100) NOT NULL,
            exit_interchange VARCHAR(100) NOT NULL,
            number_plate VARCHAR(20) NOT NULL,
            entry_time TIMESTAMP NOT NULL,
            exit_time TIMESTAMP
        )
    """
    )
    conn.commit()
    cur.close()
    conn.close()


def calculate_toll(entry_point, exit_point, entry_time, exit_time, number_plate):
    """
    Calculates the toll tax based on entry and exit points, time, and number plate.

    Args:
    - entry_point (str): The entry interchange.
    - exit_point (str): The exit interchange.
    - entry_time (datetime): The time of entry.
    - exit_time (datetime): The time of exit.
    - number_plate (str): The vehicle's number plate.

    Returns:
    - float: The calculated toll tax.
    """
    distance = calculate_distance(entry_point, exit_point)
    entry_day = entry_time.strftime("%a")
    exit_day = exit_time.strftime("%a")
    special_discount = check_special_discount(entry_day, number_plate)
    is_weekend = entry_day in ["Sat", "Sun"] or exit_day in ["Sat", "Sun"]
    is_holiday = (
        entry_time.strftime("%d-%m") in NATIONAL_HOLIDAYS
        or exit_time.strftime("%d-%m") in NATIONAL_HOLIDAYS
    )
    if is_holiday:
        total_toll = (distance * DISTANCE_RATE + BASE_TOLL_RATE) * (
            1 - HOLIDAY_DISCOUNT
        )
    else:
        if is_weekend:
            distance_rate_multiplier = WEEKEND_DISTANCE_RATE_MULTIPLIER
        else:
            distance_rate_multiplier = 1
        total_toll = (
            distance * DISTANCE_RATE * distance_rate_multiplier + BASE_TOLL_RATE
        )
        if special_discount:
            total_toll *= 0.9
    return round(total_toll, 2)


def calculate_distance(entry_point, exit_point):
    """
    Calculates the distance between entry and exit points.

    Args:
    - entry_point (str): The entry interchange.
    - exit_point (str): The exit interchange.

    Returns:
    - int: The distance between the entry and exit points.
    """
    points = {
        "Zero Point": 0,
        "NS Interchange": 5,
        "Ph4 Interchange": 10,
        "Ferozpur Interchange": 17,
        "Lake City Interchange": 24,
        "Raiwand Interchange": 29,
        "Bahria Interchange": 34,
    }
    return abs(points[exit_point] - points[entry_point])


def check_special_discount(day, number_plate):
    """
    Checks if there's a special discount for the given day and number plate.

    Args:
    - day (str): The day of the week.
    - number_plate (str): The vehicle's number plate.

    Returns:
    - bool: True if there's a special discount, False otherwise.
    """
    if day in SPECIAL_DISCOUNT_DAYS:
        if SPECIAL_DISCOUNT_DAYS[day] == "even" and int(number_plate[-1]) % 2 == 0:
            return True
        elif SPECIAL_DISCOUNT_DAYS[day] == "odd" and int(number_plate[-1]) % 2 != 0:
            return True
    return False


def validate_datetime(value):
    """
    Validates the format of a datetime string.

    Args:
    - value (str): The datetime string to validate.

    Returns:
    - datetime.datetime: The parsed datetime object.

    Raises:
    - ValueError: If the format or timezone is incorrect.
    """
    try:
        datetime_obj = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
        return datetime_obj
    except ValueError:
        raise ValueError(
            "Incorrect format or timezone. Please provide datetime"
            "in 'YYYY-MM-DDTHH:MM:SS.ssssss' format."
        )
