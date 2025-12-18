def is_manager(user):
    return user.is_authenticated and user.role == 'manager'


def is_cashier(user):
    return user.is_authenticated and user.role == 'cashier'


def is_staff(user):
    return user.is_authenticated and user.role == 'staff'
