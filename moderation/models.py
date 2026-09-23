from django.conf import settings
from django.db import models

from documents.models import Document


class Validation(models.Model):
    DECISION_CHOICES = [
        ("En attente", "En attente"),
        ("Accepté", "Accepté"),
        ("Rejeté", "Rejeté"),
        ("Archivé", "Archivé"),
    ]

    id_validation = models.AutoField(primary_key=True)
    code_validation = models.CharField(max_length=10, unique=True)
    id_document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="validations")
    id_utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="validations")
    decision = models.CharField(max_length=20, choices=DECISION_CHOICES)
    commentaire = models.TextField(blank=True, null=True)
    date_validation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_validation"]

    def __str__(self):
        return f"{self.code_validation} - {self.decision}"
