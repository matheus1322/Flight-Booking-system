from rules import predicate, predicates

@predicate
def is_admin(user):
    return user.is_authenticated and user.is_superuser

predicates.add_rule('can_view_all_bookings', predicates.is_authenticated)
predicates.add_rule('can_change_available_tickets', is_admin | predicates.is_superuser)

