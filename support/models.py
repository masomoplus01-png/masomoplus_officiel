from django.conf import settings
from django.db import models


class Support(models.Model):
    STATUT_CHOICES = [
        ("Ouvert", "Ouvert"),
        ("En cours", "En cours"),
        ("Résolu", "Résolu"),
        ("Fermé", "Fermé"),
    ]

    id_support = models.AutoField(primary_key=True)
    code_support = models.CharField(max_length=10, unique=True)
    sujet = models.CharField(max_length=200)
    message = models.TextField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default="Ouvert")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_resolution = models.DateTimeField(null=True, blank=True)
    id_utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="supports")

    class Meta:
        ordering = ["-date_creation"]

    def __str__(self):
        return self.sujet
