from django.conf import settings
from django.db import models


class Notification(models.Model):
    TYPE_CHOICES = [
        ("Validation", "Validation"),
        ("Nouveau document", "Nouveau document"),
        ("Commentaire", "Commentaire"),
        ("Collaboration", "Collaboration"),
        ("Système", "Système"),
    ]

    id_notification = models.AutoField(primary_key=True)
    code_notification = models.CharField(max_length=10, unique=True)
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    lu = models.BooleanField(default=False)
    date_notification = models.DateTimeField(auto_now_add=True)
    id_utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")

    class Meta:
        ordering = ["-date_notification"]

    def __str__(self):
        return self.titre
