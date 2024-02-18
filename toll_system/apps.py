"""
Contains AppConfig class for the toll_system Django app.

This module provides an AppConfig class for configuring the toll_system Django app.

"""

from django.apps import AppConfig


class TollSystemConfig(AppConfig):
    """
    AppConfig class for the toll_system Django app.

    Attributes:
    - default_auto_field (str): The name of the default auto field to use for models.
    - name (str): The name of the app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "toll_system"
