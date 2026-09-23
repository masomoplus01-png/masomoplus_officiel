from django.conf import settings
from django.db import models

from documents.models import Document


class Telechargement(models.Model):
    id_telechargement = models.AutoField(primary_key=True)
    code_telechargement = models.CharField(max_length=10, unique=True)
    id_document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="telechargements")
    id_utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="telechargements")
    date_telechargement = models.DateTimeField(auto_now_add=True)
    adresse_ip = models.CharField(max_length=50, blank=True, null=True)
    appareil = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.code_telechargement


class Consultation(models.Model):
    id_consultation = models.AutoField(primary_key=True)
    id_document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="consultations")
    id_utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="consultations")
    date_consultation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Consultation {self.id_consultation}"


class Favori(models.Model):
    id_favori = models.AutoField(primary_key=True)
    id_document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="favoris")
    id_utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favoris")
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("id_document", "id_utilisateur")

    def __str__(self):
        return f"Favori {self.id_document_id} - {self.id_utilisateur_id}"


class Commentaire(models.Model):
    id_commentaire = models.AutoField(primary_key=True)
    id_document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="commentaires")
    id_utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="commentaires")
    contenu = models.TextField()
    date_commentaire = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commentaire {self.id_commentaire}"
