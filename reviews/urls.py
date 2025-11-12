from django.urls import path
from . import views

urlpatterns = [
    path('flux/',views.feed_view, name='feed'),
    path('create_ticket/', views.create_ticket, name='create_ticket'), 
    path('ticket_succes/', views.ticket_succes, name='ticket_succes'),
    path('ticket/<int:ticket_id>/edit/',views.edit_ticket, name='edit_ticket'),
    path('delete_ticket/<int:ticket_id>/',views.delete_ticket, name='delete_ticket'),
    path('ticket/<int:ticket_id>/review/', views.create_review, name='create_review'),
    path('select_ticket_to_review/', views.select_ticket_to_review, name='select_ticket_to_review'),
    path('create_review/', views.create_ticket_and_review, name='create_ticket_and_review'),
]