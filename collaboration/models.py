from django.conf import settings
from django.db import models


class Projet(models.Model):
    STATUT_CHOICES = [
        ("Ouvert", "Ouvert"),
        ("En cours", "En cours"),
        ("Fermé", "Fermé"),
    ]

    id_projet = models.AutoField(primary_key=True)
    code_projet = models.CharField(max_length=10, unique=True)
    titre = models.CharField(max_length=200)
    description = models.TextField()
    domaine = models.CharField(max_length=100)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default="Ouvert")
    date_creation = models.DateTimeField(auto_now_add=True)
    id_createur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="projets_crees")

    class Meta:
        ordering = ["-date_creation"]

    def __str__(self):
        return self.titre
