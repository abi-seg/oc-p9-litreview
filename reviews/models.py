from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

class Review(models.Model):
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE) # à créer !
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.headline} - {self.user.username}"

class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048,blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"
    
class UserFollows(models.Model):
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
