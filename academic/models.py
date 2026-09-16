from django.db import models


class Faculté(models.Model):
    code_faculte = models.CharField(max_length=10, unique=True)
    nom = models.CharField(max_length=150)
    déscription = models.TextField(blank=True)

    def __str__(self):
        return f"{self.code_faculte} - {self.nom}"


class Département(models.Model):
    code_departement = models.CharField(max_length=10, unique=True)
    nom = models.CharField(max_length=150)
    déscription = models.TextField(blank=True)
    faculte = models.ForeignKey(
        Faculté,
        on_delete=models.CASCADE,
        related_name="départements"
    )

    def __str__(self):
        return f"{self.code_departement} - {self.nom}"


class Filière(models.Model):
    code_filiere = models.CharField(max_length=10, unique=True)
    nom = models.CharField(max_length=150)
    déscription = models.TextField(blank=True)
    département = models.ForeignKey(
        Département,
        on_delete=models.CASCADE,
        related_name="filières"
    )

    def __str__(self):
        return f"{self.code_filiere} - {self.nom}"


class Categorie(models.Model):
    code_categorie = models.CharField(max_length=10, unique=True)
    nom = models.CharField(max_length=100)
    déscription = models.TextField(blank=True)

    def __str__(self):
        return f"{self.code_categorie} - {self.nom}"