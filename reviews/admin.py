from django.contrib import admin
from .models import Ticket, UserFollows  # and other models like Review


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title','user','time_created')
    search_fields = ('title', 'user__username')
    list_filter = ('user',)

@admin.register(UserFollows)
class UserFollowsAdmin(admin.ModelAdmin):
    list_display = ('user', 'followed_user')
    search_fields = ('user__username','followed_user__username')

# Register your models here.
