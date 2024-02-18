"""
Contains constants for the toll_system Django app.

"""

BASE_TOLL_RATE = 20
DISTANCE_RATE = 0.2
WEEKEND_DISTANCE_RATE_MULTIPLIER = 1.5
SPECIAL_DISCOUNT_DAYS = {
    "Mon": "even",
    "Tue": "odd",
    "Wed": "even",
    "Thu": "odd",
}
NATIONAL_HOLIDAYS = ["23-03", "14-08", "25-12"]
HOLIDAY_DISCOUNT = 0.5
