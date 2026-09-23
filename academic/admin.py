from django.contrib import admin
from .models import Faculté, Département, Filière, Categorie
# Register your models here.

@admin.register(Faculté)
class FacultéAdmin(admin.ModelAdmin):
    list_display = ("id", "code_faculte", "nom")
    search_fields = ("code_faculte", "nom")


@admin.register(Département)
class DépartementAdmin(admin.ModelAdmin):
    list_display = ("id", "code_departement", "nom", "faculte")
    search_fields = ("code_departement", "nom")
    list_filter = ("faculte",)


@admin.register(Filière)
class FilièreAdmin(admin.ModelAdmin):
    list_display = ("id", "code_filiere", "nom", "département")
    search_fields = ("code_filiere", "nom")
    list_filter = ("département",)


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ("id", "code_categorie", "nom")
    search_fields = ("code_categorie", "nom")
