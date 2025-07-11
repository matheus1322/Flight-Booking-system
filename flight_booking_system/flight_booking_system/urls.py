"""
URL configuration for flight_booking_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from flight_booking.views import (
    book_ticket, cancel_ticket, submit_feedback, export_reports_view, home, available_tickets, search_tickets, ticket_details, feedback_list, delete_feedback, reply_feedback, edit_feedback, submit_reply, submit_edit, submit_delete
)
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Add the accounts URLs for authentication
    path('available-tickets/', available_tickets, name='available_tickets'),
    path('book-ticket/', book_ticket, name='book_ticket'),
    path('book-ticket/ticket_details/<int:booking_id>/', ticket_details, name='ticket_details'),
    path('cancel-ticket/', cancel_ticket, name='cancel_ticket'),
    path('submit-feedback/', submit_feedback, name='submit_feedback'),
    path('feedback-list/', feedback_list, name='feedback_list'),
    path('export_reports/', export_reports_view, name='export_reports'),  # Update the URL for exporting reports
    path('export-reports/csv/', export_reports_view, {'file_format': 'csv'}, name='export_reports_csv'),  # Update the URL for exporting CSV reports
    path('export-reports/txt/', export_reports_view, {'file_format': 'txt'}, name='export_reports_txt'),  # Update the URL for exporting text reports
    path('', home, name='home'),
    path('search_tickets/', search_tickets, name='search_tickets'),
    path('__debug__/', include('debug_toolbar.urls')),
    path('edit-feedback/<int:feedback_id>/', edit_feedback, name='edit_feedback'),
    path('reply-feedback/<int:feedback_id>/', reply_feedback, name='reply_feedback'),
    path('delete-feedback/<int:feedback_id>/', delete_feedback, name='delete_feedback'),
    path('submit-reply/<int:feedback_id>/', submit_reply, name='submit_reply'),
    path('submit-edit/<int:feedback_id>/', submit_edit, name='submit_edit'),
    path('submit-delete/<int:feedback_id>/', submit_delete, name='submit_delete'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


