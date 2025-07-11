import csv
from django.contrib import admin
from django.db.models import Sum
from django.http import HttpResponse
from django.urls import path
from django.shortcuts import render
from .models import Ticket, Booking


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'ticket_type', 'availability', 'price')

    def get_ticket_code(self, obj):
        return obj.ticket_code

    get_ticket_code.short_description = 'Ticket Code'

    def total_tickets_sold(self, obj):
        total_sold = Ticket.objects.aggregate(total_sold=Sum('availability'))['total_sold']
        return total_sold or 0

    def total_income(self, obj):
        total_income = Ticket.objects.aggregate(total_income=Sum('price'))['total_income']
        return total_income or 0

    def income_per_type(self, obj):
        ticket_types = ['Economy', 'First Class', 'Premium Economy']
        income_per_type = {}
        for ticket_type in ticket_types:
            total_income = Ticket.objects.filter(ticket_type=ticket_type).aggregate(total_income=Sum('price'))['total_income']
            income_per_type[ticket_type] = total_income or 0
        return income_per_type


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'ticket_code', 'username', 'number_of_tickets_economy', 'number_of_tickets_first_class', 'number_of_tickets_premium_economy', 'total_price')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('export-reports/', self.export_reports_view, name='export_reports'),
        ]
        return custom_urls + urls

    def export_reports_view(self, request):
        if not request.user.is_superuser:
            return HttpResponse("You are not authorized to access this page.")

        if request.method == 'POST':
            format = request.POST.get('format')
            if format == 'csv':
                response = self.export_csv()
                return response
            elif format == 'text':
                response = self.export_text()
                return response
        else:
            return render(request, 'export_reports.html')

    def export_csv(self):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="report.csv"'
        writer = csv.writer(response)
        writer.writerow(['Ticket Type', 'Quantity', 'Income'])
        ticket_types = ['Economy', 'First Class', 'Premium Economy']
        for ticket_type in ticket_types:
            total_sold = Booking.objects.filter(ticket__ticket_type=ticket_type).aggregate(total_sold=Sum('number_of_tickets_economy', 'number_of_tickets_first_class', 'number_of_tickets_premium_economy'))['total_sold']
            total_income = Booking.objects.filter(ticket__ticket_type=ticket_type).aggregate(total_income=Sum('total_price'))['total_income']
            writer.writerow([ticket_type, total_sold or 0, total_income or 0])
        return response

    def export_text(self):
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="report.txt"'
        ticket_types = ['Economy', 'First Class', 'Premium Economy']
        for ticket_type in ticket_types:
            total_sold = Booking.objects.filter(ticket__ticket_type=ticket_type).aggregate(total_sold=Sum('number_of_tickets_economy', 'number_of_tickets_first_class', 'number_of_tickets_premium_economy'))['total_sold']
            total_income = Booking.objects.filter(ticket__ticket_type=ticket_type).aggregate(total_income=Sum('total_price'))['total_income']
            response.write(f'Ticket Type: {ticket_type}\n')
            response.write(f'Quantity: {total_sold or 0}\n')
            response.write(f'Income: {total_income or 0}\n')
            response.write('\n')

        return response
