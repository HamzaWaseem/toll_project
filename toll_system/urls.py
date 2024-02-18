"""
Defines URL patterns for the toll system app.

The urlpatterns list routes URLs to views in the toll system app.
"""

from django.urls import path
from . import views

urlpatterns = [
    path("entry", views.entry, name="entry"),
    path("exit", views.exit, name="exit"),
]
