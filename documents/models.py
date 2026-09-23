from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from academic.models import Categorie, Filière


class Document(models.Model):
    STATUS_CHOICES = [
        ("Brouillon", "Brouillon"),
        ("Attente", "Attente"),
        ("Validé", "Validé"),
        ("Rejeté", "Rejeté"),
    ]

    id_document = models.AutoField(primary_key=True)
    code_document = models.CharField(max_length=10, unique=True)
    titre = models.CharField(max_length=255)
    resume = models.TextField()
    mots_cles = models.TextField(blank=True, default="")
    fichier = models.FileField(upload_to="documents/pdfs/")
    couverture = models.ImageField(upload_to="documents/couvertures/", blank=True, null=True)
    annee_publication = models.PositiveIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2100)]
    )
    langue = models.CharField(max_length=30, blank=True, null=True)
    nombre_pages = models.PositiveIntegerField(blank=True, null=True)
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Brouillon")
    date_depot = models.DateTimeField(auto_now_add=True)
    id_categorie = models.ForeignKey(Categorie, on_delete=models.PROTECT, related_name="documents")
    id_filiere = models.ForeignKey(Filière, on_delete=models.PROTECT, related_name="documents")
    id_utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="documents"
    )

    class Meta:
        ordering = ["-date_depot"]

    def clean(self):
        super().clean()
        if self.fichier and not str(self.fichier.name).lower().endswith(".pdf"):
            raise ValidationError({"fichier": "Seuls les fichiers PDF sont autorisés."})

        if self.couverture and not str(self.couverture.name).lower().endswith(
            (".jpg", ".jpeg", ".png", ".webp")
        ):
            raise ValidationError({"couverture": "Seules les images JPG, JPEG, PNG ou WEBP sont autorisées."})

    def __str__(self):
        return self.titre
