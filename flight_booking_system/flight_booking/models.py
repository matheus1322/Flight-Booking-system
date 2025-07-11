from django.db import models
import random
import string


class Ticket(models.Model):
    TICKET_TYPES = [
        ('economy', 'Economy'),
        ('first_class', 'First Class'),
        ('premium_economy', 'Premium Economy')
    ]

    ticket_type = models.CharField(max_length=20, choices=TICKET_TYPES, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    availability = models.PositiveIntegerField()

    def __str__(self):
        return self.ticket_type


class Booking(models.Model):
    username = models.CharField(max_length=100, default='')
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    number_of_tickets = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    ticket_code = models.CharField(max_length=6)
    number_of_tickets_economy = models.PositiveIntegerField(default=0)
    number_of_tickets_first_class = models.PositiveIntegerField(default=0)
    number_of_tickets_premium_economy = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Booking #{self.pk}"

    def save(self, *args, **kwargs):
        if not self.ticket_code:
            self.ticket_code = self._generate_ticket_code()
        return super().save(*args, **kwargs)

    def _generate_ticket_code(self):
        # Generate a random code with length 6
        code_length = 6
        characters = string.ascii_letters + string.digits
        return ''.join(random.choices(characters, k=code_length))


class Feedback(models.Model):
    username = models.CharField(max_length=100, default='')
    feedback = models.TextField()
    reply = models.OneToOneField('Reply', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        if self.reply:
            return f"Username: {self.username}\nFeedback: {self.feedback}\nReply: {self.reply.content}"
        else:
            return f"Username: {self.username}\nFeedback: {self.feedback}"


class Reply(models.Model):
    content = models.TextField()

    def __str__(self):
        return self.content
    
