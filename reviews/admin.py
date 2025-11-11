from django.contrib import admin
from .models import Ticket  # and other models like Review


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title','user','time_created')
    search_fields = ('title', 'user__username')
    list_filter = ('user',)

# Register your models here.
