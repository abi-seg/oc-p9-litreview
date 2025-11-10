from django.urls import path
from . import views

urlpatterns = [
    path('flux/',views.feed_view, name='feed'),
]