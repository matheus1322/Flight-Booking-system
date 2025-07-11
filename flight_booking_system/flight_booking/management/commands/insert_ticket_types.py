from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Insert ticket types into the database.'

    def handle(self, *args, **options):
        query = """
            INSERT INTO ticket_types (ticket_type, availability)
            VALUES
                ('economy', 100),
                ('first_class', 50),
                ('premium_economy', 75)
        """

        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()

        self.stdout.write(self.style.SUCCESS('Ticket types inserted successfully.'))
