from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('connexion/', views.connexion_view, name='connexion'),
    path('inscription/', views.inscription_view, name='inscription'),
    path('login/',views.connexion_view, name='login'),
    path('logout/',LogoutView.as_view(), name='logout'),
]