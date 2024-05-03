from django.contrib import admin
from .models import Queue, Ticket


class QueueAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'createdAt', 'modifiedAt')
    readonly_fields  = ('createdAt', 'modifiedAt')

class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'queue', 'number', 'status', 'createdAt', 'modifiedAt')
    readonly_fields  = ('createdAt', 'modifiedAt')

admin.site.register(Queue, QueueAdmin)
admin.site.register(Ticket, TicketAdmin)