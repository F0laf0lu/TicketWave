from django.urls import path
from . import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

API_TITLE = 'TIcketave API'
API_TITLE = 'Ticketave API'
schema_view = get_schema_view(
    openapi.Info(
        title=API_TITLE,
        default_version='v1',
    ),
)

urlpatterns = [
    path('events/', views.events, name="events"),
    path('events/<int:event_id>/', views.event_detail, name="event-detail"),
    path('events/<int:event_id>/tickets/', views.event_tickets, name="event-ticket"),
    path('events/<int:event_id>/get_ticket/', views.get_ticket, name="get-ticket"),
    path('ticket/', views.tickets, name="ticket"),
    path('ticket/<int:ticket_id>/', views.ticket_detail, name="ticket-detail"),
    path('swagger-docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

