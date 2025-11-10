from django.urls import path
from . import views

urlpatterns = [
    path('connexion/', views.connexion_view, name='connexion'),
    path('inscription/', views.inscription_view, name='inscription'),
    path('login/',views.connexion_view, name='login'),
]