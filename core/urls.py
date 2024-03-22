from django.urls import path
from . import views



urlpatterns = [
    path('events/', views.events, name="events"),
    path('events/<int:event_id>/', views.event_detail, name="event-detail"),
    path('events/<int:event_id>/tickets/', views.event_tickets, name="event-ticket"),
    path('events/<int:event_id>/get_ticket/', views.get_ticket, name="get-ticket"),
    path('ticket/', views.tickets, name="ticket"),
    path('ticket/<int:ticket_id>/', views.ticket_detail, name="ticket-detail"),
]

