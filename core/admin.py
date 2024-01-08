from django.contrib import admin
from core.models import Event, Ticket, TicketType
# Register your models here.


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'organizer', 'event_status', 'event_date', 'event_time']

    def event_status(self, obj):
        return dict(Event.STATUS).get(obj.status, obj.status)
    
    def event_date(self, obj):
        return obj.time.date()
    
    def event_time(self, obj):
        return obj.time.time()
    
    event_status.short_description = 'Status'
    event_time.short_description = 'Time'
    event_date.short_description = 'Date'


# admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(TicketType)