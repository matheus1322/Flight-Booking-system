from django import forms
from .models import Booking
from .models import Feedback



class TicketBookingForm(forms.Form):
    username = forms.CharField(label='Username')
    number_of_tickets_economy = forms.IntegerField(label='Economy', min_value=0)
    number_of_tickets_first_class = forms.IntegerField(label='First Class', min_value=0)
    number_of_tickets_premium_economy = forms.IntegerField(label='Premium Economy', min_value=0)


class TicketCancellationForm(forms.Form):
    ticket_code = forms.CharField(label='Ticket Code')


class FeedbackSubmissionForm(forms.Form):
    username = forms.CharField(label='Username')
    feedback = forms.CharField(label='Feedback', widget=forms.Textarea)


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['username','ticket', 'number_of_tickets', 'total_price', 'ticket_code']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['username', 'feedback']
        
class ReplyForm(forms.Form):
    reply = forms.CharField(widget = forms.Textarea)

class EditForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback']


        
        