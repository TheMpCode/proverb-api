from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True) # LE NOM D'UTILISATEUR DOIT ÊTRE UNIQUE
    avatar = models.URLField(blank=True, null=True)
    email = models.EmailField(unique=True) # UNE ADRESSE EMAIL UNIQUE POUR CHAQUE UTILISATEUR

    REQUIRED_FIELDS = ['email'] # L'EMAIL EST UN CHAMP OBLIGATOIRE POUR LA CRÉATION D'UN UTILISATEUR


    def __str__(self):
        return self.username