from django.contrib import admin
from core.models import Event, Ticket, TicketType
# Register your models here.


admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(TicketType)