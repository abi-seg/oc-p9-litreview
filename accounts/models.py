from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Modèle utilisateur personnalisé (hérite d'AbstractUser).
    Vous pouvez ajouter des champs supplémentaires ici si nécessaire.
    """
    pass
