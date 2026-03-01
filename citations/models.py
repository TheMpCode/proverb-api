from operator import add

from django.db import models
from django.conf import settings



class Author(models.Model):
    """MODELE DE REPRESENTATION D'UN AUTEUR DE CITATIONS"""

    name = models.CharField(max_length=255, unique=True)
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    death_date = models.DateField(blank=True, null=True)
    
    # ==> AJOUT D'UN INDEX SURE LE NOM POUR LES RECHERCHES RAPIDES
    class Meta:
        indexes = [models.Index(fields=['name'])]


    def __str__(self):
        return self.name
    


class Citation(models.Model):
    """ MODELE DE REPRESENTATION D'UNE CITATION """

    text = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.PROTECT,
                                        related_name='citations')
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # ==> SUIVI TEMPOREL
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ==> EVITER LES DUPLICATS DE CITATIONS POUR UN MEME AUTEUR
    # ==> UTILISATION D'UNE CONTRAINTE D'UNICITE COMBINEE
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['text', 'author'],
                                        name='unique_citation_per_author')
        ]

        indexes = [
            models.Index(fields=['created_at']),
        ]


    def save(self, *args, **kwargs):
        """ SURCHARGE DE LA METHODE DE SAUVEGARDE POUR NORMALISER LE TEXTE DE LA CITATION """

        self.text = self.text.strip()
        super().save(*args, **kwargs)

