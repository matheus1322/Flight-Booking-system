from django.core.management.base import BaseCommand
from flight_booking.models import Ticket


class Command(BaseCommand):
    help = 'Creates initial tickets in the database'

    def handle(self, *args, **options):
        tickets_data = [
            {'ticket_type': 'economy', 'availability': 30},
            {'ticket_type': 'premium_economy', 'availability': 20},
            {'ticket_type': 'first_class', 'availability': 10},
        ]

        for ticket_data in tickets_data:
            ticket = Ticket(**ticket_data)
            ticket.save()

        self.stdout.write(self.style.SUCCESS('Successfully created initial tickets.'))
