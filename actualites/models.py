from django.conf import settings
from django.db import models


class Actualite(models.Model):
    id_actualite = models.AutoField(primary_key=True)
    code_actualite = models.CharField(max_length=10, unique=True)
    titre = models.CharField(max_length=255)
    contenu = models.TextField()
    image = models.ImageField(upload_to="actualites/images/", blank=True, null=True)
    date_publication = models.DateTimeField(auto_now_add=True)
    id_auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="actualites")

    class Meta:
        ordering = ["-date_publication"]

    def __str__(self):
        return self.titre
