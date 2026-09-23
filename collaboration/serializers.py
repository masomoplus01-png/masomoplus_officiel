from rest_framework import serializers

from .models import Projet


class ProjetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projet
        fields = [
            "id_projet",
            "code_projet",
            "titre",
            "description",
            "domaine",
            "statut",
            "date_creation",
            "id_createur",
        ]
        read_only_fields = ["id_projet", "date_creation", "id_createur"]

    def validate_code_projet(self, value):
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError("Le code_projet est invalide.")
        return value
