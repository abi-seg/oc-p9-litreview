from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Enregistrement du modèle utilisateur personnalisé dans l'admin
admin.site.register(CustomUser, UserAdmin)

