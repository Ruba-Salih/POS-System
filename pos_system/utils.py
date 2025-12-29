from datetime import datetime, time, timedelta
from django.utils.timezone import make_aware

def business_day_range(date):
    """
    Returns start and end datetime for a business day starting at 5am.
    """

    start = datetime.combine(date, time(5, 0))          # 05:00 AM
    end = start + timedelta(days=1)                     # next day 05:00 AM

    start = make_aware(start)
    end = make_aware(end)

    return start, end

def is_manager(user):
    return user.is_authenticated and user.role == 'manager'


def is_cashier(user):
    return user.is_authenticated and user.role == 'cashier'


def is_staff(user):
    return user.is_authenticated and user.role == 'staff'
