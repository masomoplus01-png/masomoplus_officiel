from rest_framework import serializers

from .models import Support


class SupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Support
        fields = [
            "id_support",
            "code_support",
            "sujet",
            "message",
            "statut",
            "date_creation",
            "date_resolution",
            "id_utilisateur",
        ]
        read_only_fields = ["id_support", "date_creation", "date_resolution", "id_utilisateur"]
