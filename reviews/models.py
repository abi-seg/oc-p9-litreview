from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

class Review(models.Model):
    """
    Modèle représentant une critique (review) laissée par un utilisateur.

    Chaque critique est associée à un ticket et contient :
    - une note (entre 1 et 5),
    - un titre court (headline),
    - un corps de texte facultatif (body),
    - une référence à l'utilisateur qui a rédigé la critique,
    - une date de création automatiquement enregistrée.

    La relation entre Review et Ticket est une relation 1-N :
    un ticket peut recevoir plusieurs critiques.

    """
    RATING_CHOICES = [(i, str(i)) for i in range(1,6)]
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE) # à créer !
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.headline} - {self.user.username}"

class Ticket(models.Model):
    """
    Modèle représentant un ticket publié par un utilisateur.

    Un ticket correspond à une demande de critique. Il contient :
    - un titre,
    - une description optionnelle,
    - une image facultative,
    - l'utilisateur à l'origine du ticket,
    - la date de création.

    Les critiques (Review) sont liées à ce ticket via une clé étrangère.

    """
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048,blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='ticket_images/',null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"
    
class UserFollows(models.Model):
    """
    Modèle représentant une relation de suivi entre utilisateurs.

    Ce modèle stocke :
    - l'utilisateur qui suit (user),
    - l'utilisateur qui est suivi (followed_user).

    La contrainte 'unique_together' empêche un utilisateur de suivre
    plusieurs fois la même personne. Les relations sont définies via des
    clés étrangères vers le modèle utilisateur personnalisé.
    
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='following' # celui qui suit quelqu'un

    )
    followed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followed_by' # celui qui est suivi

    )

    class Meta:
        unique_together = ('user','followed_user')
        verbose_name = "User follow"
        verbose_name_plural = "User follows"

    def __str__(self):
        return f"{self.user.username} follows {self.followed_user.username}"

# Create your models here.
