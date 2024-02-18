"""
Contains models for the toll_system Django app.

"""

from django.db import models


class TollData(models.Model):
    """
    Model to represent toll data.

    Attributes:
    - entry_interchange (str): The interchange where the vehicle entered.
    - exit_interchange (str): The interchange where the vehicle exited (optional).
    - number_plate (str): The vehicle's number plate.
    - entry_time (datetime): The time when the vehicle entered.
    - exit_time (datetime, optional): The time when the vehicle exited (optional).
    """

    entry_interchange = models.CharField(max_length=100)
    exit_interchange = models.CharField(max_length=100, blank=True, null=True)
    number_plate = models.CharField(max_length=20)
    entry_time = models.DateTimeField()
    exit_time = models.DateTimeField(blank=True, null=True)
