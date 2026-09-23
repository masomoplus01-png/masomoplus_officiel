from rest_framework import serializers

from .models import Auteur, DocumentAuteur


class AuteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auteur
        fields = (
            "id_auteur",
            "code_auteur",
            "nom",
            "postnom",
            "prenom",
            "email",
            "affiliation",
            "biographie",
            "orcid",
        )
        read_only_fields = ("id_auteur",)


class DocumentAuteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentAuteur
        fields = (
            "id_document_auteur",
            "id_document",
            "id_auteur",
            "ordre_auteur",
            "role_auteur",
        )
        read_only_fields = ("id_document_auteur",)
