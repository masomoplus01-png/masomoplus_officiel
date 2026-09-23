from rest_framework import serializers

from .models import Commentaire, Consultation, Favori, Telechargement


class TelechargementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Telechargement
        fields = (
            "id_telechargement",
            "code_telechargement",
            "id_document",
            "id_utilisateur",
            "date_telechargement",
            "adresse_ip",
            "appareil",
        )
        read_only_fields = ("id_telechargement", "date_telechargement", "id_utilisateur")


class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = (
            "id_consultation",
            "id_document",
            "id_utilisateur",
            "date_consultation",
        )
        read_only_fields = ("id_consultation", "date_consultation", "id_utilisateur")


class FavoriSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favori
        fields = (
            "id_favori",
            "id_document",
            "id_utilisateur",
            "date_ajout",
        )
        read_only_fields = ("id_favori", "date_ajout", "id_utilisateur")


class CommentaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentaire
        fields = (
            "id_commentaire",
            "id_document",
            "id_utilisateur",
            "contenu",
            "date_commentaire",
        )
        read_only_fields = ("id_commentaire", "date_commentaire", "id_utilisateur")
