from django.db import models

from documents.models import Document


class Auteur(models.Model):
    id_auteur = models.AutoField(primary_key=True)
    code_auteur = models.CharField(max_length=10, unique=True)
    nom = models.CharField(max_length=100)
    postnom = models.CharField(max_length=100, blank=True, null=True)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(max_length=150, blank=True, null=True)
    affiliation = models.CharField(max_length=200, blank=True, null=True)
    biographie = models.TextField(blank=True, null=True)
    orcid = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        ordering = ["nom", "prenom"]

    def __str__(self):
        return f"{self.nom} {self.prenom}".strip()


class DocumentAuteur(models.Model):
    ROLE_CHOICES = [
        ("Auteur", "Auteur"),
        ("Co-auteur", "Co-auteur"),
        ("Directeur", "Directeur"),
        ("Encadreur", "Encadreur"),
    ]

    id_document_auteur = models.AutoField(primary_key=True)
    id_document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="document_auteurs")
    id_auteur = models.ForeignKey(Auteur, on_delete=models.CASCADE, related_name="document_auteurs")
    ordre_auteur = models.SmallIntegerField()
    role_auteur = models.CharField(max_length=30, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ("id_document", "id_auteur")
        ordering = ["ordre_auteur"]

    def __str__(self):
        return f"{self.id_auteur} - {self.id_document}"
