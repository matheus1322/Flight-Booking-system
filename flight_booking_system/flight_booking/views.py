import sys
from django.shortcuts import render, redirect, get_object_or_404
from flight_booking.models import Ticket, Booking, Feedback, Reply
from django.contrib import messages
import string
import random
from django.http import HttpResponse
from .forms import TicketBookingForm, FeedbackSubmissionForm, FeedbackForm
from decimal import Decimal, ROUND_DOWN
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
import pandas as pd
from django.urls import reverse

sys.path.append('C:/Users/Matheus/Desktop/Coding/flight_booking_system')

def home(request):
    return render(request, 'flight_booking/home.html')


def book_ticket(request):
    tickets = Ticket.objects.all()
    form = TicketBookingForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            num_tickets_economy = form.cleaned_data['number_of_tickets_economy']
            num_tickets_first_class = form.cleaned_data['number_of_tickets_first_class']
            num_tickets_premium_economy = form.cleaned_data['number_of_tickets_premium_economy']

            try:
                ticket_economy = tickets.get(ticket_type='economy')
                ticket_first_class = tickets.get(ticket_type='first_class')
                ticket_premium_economy = tickets.get(ticket_type='premium_economy')

                num_tickets_total = (
                    num_tickets_economy + num_tickets_first_class + num_tickets_premium_economy
                )

                if (
                    ticket_economy.availability >= num_tickets_economy
                    and ticket_first_class.availability >= num_tickets_first_class
                    and ticket_premium_economy.availability >= num_tickets_premium_economy
                ):
                    total_price_economy = ticket_economy.price * num_tickets_economy
                    total_price_first_class = ticket_first_class.price * num_tickets_first_class
                    total_price_premium_economy = ticket_premium_economy.price * num_tickets_premium_economy

                    total_price = (
                        total_price_economy + total_price_first_class + total_price_premium_economy
                    )

                    discounted_price = apply_discount(num_tickets_total, total_price)

                    ticket_economy.availability -= num_tickets_economy
                    ticket_first_class.availability -= num_tickets_first_class
                    ticket_premium_economy.availability -= num_tickets_premium_economy

                    ticket_economy.save()
                    ticket_first_class.save()
                    ticket_premium_economy.save()

                    booking = Booking.objects.create(
                        username=form.cleaned_data['username'],
                        ticket=ticket_economy,
                        number_of_tickets_economy=num_tickets_economy,
                        number_of_tickets_first_class=num_tickets_first_class,
                        number_of_tickets_premium_economy=num_tickets_premium_economy,
                        number_of_tickets=num_tickets_total,
                        total_price=discounted_price,
                        ticket_code=generate_ticket_code(),
                    )
                    booking.save()

                    return redirect('ticket_details', booking_id=booking.id)

                else:
                    messages.error(request, 'Insufficient ticket availability.')
            except Ticket.DoesNotExist:
                messages.error(request, 'Tickets not available.')

    context = {
        'tickets': tickets,
        'form': form,
    }

    return render(request, 'book_ticket.html', context)


def apply_discount(num_tickets, total_price):
    if num_tickets >= 5:
        discount = Decimal(0.2)  # 20% discount
        discount_amount = total_price * discount
        discounted_price = total_price - discount_amount

        return discounted_price.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

    return total_price


def generate_ticket_code():
    characters = string.ascii_uppercase + string.digits
    ticket_code = ''.join(random.choices(characters, k=6))

    while Booking.objects.filter(ticket_code=ticket_code).exists():
        ticket_code = ''.join(random.choices(characters, k=6))

    return ticket_code


def available_tickets(request):
    tickets = Ticket.objects.all()
    return render(request, 'available_tickets.html', {'tickets': tickets})


def ticket_details(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    context = {'booking': booking}
    return render(request, 'ticket_details.html', context)


def cancel_ticket(request):
    if request.method == 'POST':
        ticket_code = request.POST.get('ticket_code')
        try:
            booking = Booking.objects.get(ticket_code=ticket_code)
            ticket = booking.ticket

            ticket.availability += booking.number_of_tickets
            ticket.save()

            booking.delete()

            messages.success(request, 'Your ticket has been cancelled successfully!')
            return redirect('cancel_ticket')

        except Booking.DoesNotExist:
            messages.error(request, 'Invalid ticket code.')

    return render(request, 'cancel_ticket.html')


def search_tickets(request):
    ticket_code = request.GET.get('ticket_code')
    bookings = Booking.objects.filter(ticket_code=ticket_code) if ticket_code else None

    if bookings:
        messages.success(request, 'This is your ticket!')
    else:
        messages.error(request, 'Invalid ticket code. Please try again.')

    return render(request, 'search_tickets.html', {'bookings': bookings})

@login_required
def display_bookings(request):
    if request.user.is_superuser:
        bookings = Booking.objects.all()
        return render(request, 'display_bookings.html', {'bookings': bookings})
    else:
        return render(request, 'access_denied.html')

def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackSubmissionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            feedback = form.cleaned_data['feedback']
            
            feedback = Feedback(username=username, feedback=feedback)
            feedback.save()
            messages.success(request, 'Thank you for your Feedback!')
            return redirect('feedback_list')
            
            if not username:
                messages.error(request, 'Please fill in your username.')
            elif not feedback:
                messages.error(request, 'Please provide your feedback.')
    else:
        form = FeedbackSubmissionForm()

    return render(request, 'submit_feedback.html', {'form': form})


def feedback_list(request):
    feedbacks = Feedback.objects.prefetch_related()
    context = {'feedbacks': feedbacks}
    return render(request, 'submit_feedback.html', context)





@login_required
@staff_member_required
def edit_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)

    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            return redirect('feedback_list')
    else:
        form = FeedbackForm(instance=feedback)

    context = {'feedback': feedback, 'form': form}
    return render(request, 'edit_feedback.html', context)



@login_required
@staff_member_required
def reply_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)

    if request.method == 'POST':
        reply_content = request.POST.get('reply')
        reply = Reply(content=reply_content)
        reply.save()
        feedback.reply = reply
        feedback.save()
        return redirect('feedback_list')

    context = {'feedback': feedback}
    return render(request, 'reply_feedback.html', context)

@login_required
@staff_member_required
def delete_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)

    if request.method == 'POST':
        feedback.delete()
        return redirect('feedback_list')

    context = {'feedback': feedback}
    return render(request, 'delete_feedback.html', context)



@staff_member_required(login_url='/admin/login/') 
def export_reports_view(request):
    if request.method == 'POST':
        file_format = request.POST.get('format')

        bookings = Booking.objects.all()
        
        #Create a list of dictionariescontaing data
        data = [
            {
                'Ticket Code': booking.ticket_code,
                'Username': booking.username,
                'Economy Tickets': booking.number_of_tickets_economy,
                'First Class Tickets': booking.number_of_tickets_first_class,
                'Premium Economy Tickets': booking.number_of_tickets_premium_economy,
                'Number of Tickets': booking.number_of_tickets,
                'Total Price': booking.total_price,
            }
            for booking in bookings
        ]

        df = pd.DataFrame(data)

        if file_format == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="bookings.csv"'
            df.to_csv(response, index=False)
        elif file_format == 'text':
            response = HttpResponse(content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename="bookings.txt"'
            df.to_string(response, index=False)
       

        return response

    
    return render(request, 'export_reports.html')



def submit_reply(request, feedback_id):
    if request.method == 'POST':
        feedback = get_object_or_404(Feedback, id=feedback_id)
        reply = request.POST.get('reply')
        
        # Update the feedback with the reply
        feedback.reply = reply
        feedback.save()
        
        # Redirect to the feedback list view
        return redirect('feedback_list')

def show_reply(request, reply_id):
    reply = Reply.objects.get(id=reply_id)
    context = {'reply': reply}
    return render(request, 'feedback_list.html', context)


def submit_edit(request, feedback_id):
    if request.method == 'POST':
        feedback = get_object_or_404(Feedback, id=feedback_id)
        edited_feedback = request.POST.get('edited_feedback', '')
        
        feedback.feedback = edited_feedback
        feedback.save()
        
        return redirect('feedback_list')

    return HttpResponse()

def show_edit(request, feedback_id):
    feedback = Feedback.objects.get(id=feedback_id)
    context = {'feedback': feedback}
    return render(request, 'feedback_list.html', context)

def submit_delete(request, feedback_id):
    if request.method == 'POST':
        feedback = get_object_or_404(Feedback, id=feedback_id)
        feedback.delete()
        
        return redirect('feedback_list')

    return HttpResponse()
