from django.urls import path
from . import views

urlpatterns = [
    path('flux/',views.feed_view, name='feed'),
    path('create_ticket/', views.create_ticket, name='create_ticket'), 
    path('ticket_succes/', views.ticket_succes, name='ticket_succes'),
]