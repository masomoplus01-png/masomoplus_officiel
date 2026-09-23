from rest_framework import serializers

from documents.models import Document
from .models import Validation


class ValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Validation
        fields = (
            "id_validation",
            "code_validation",
            "id_document",
            "id_utilisateur",
            "decision",
            "commentaire",
            "date_validation",
        )
        read_only_fields = ("id_validation", "date_validation", "id_utilisateur")

    def validate(self, attrs):
        document = attrs.get("id_document")
        decision = attrs.get("decision")
        current_status = document.statut if document else None

        allowed = {
            "Brouillon": ["En attente"],
            "En attente": ["Accepté", "Rejeté"],
            "Accepté": ["Archivé"],
            "Rejeté": [],
            "Archivé": [],
        }

        if current_status not in allowed:
            raise serializers.ValidationError({"decision": "Statut non pris en charge pour validation."})

        if decision not in allowed.get(current_status, []):
            raise serializers.ValidationError({"decision": "Transition invalide pour le workflow de validation."})

        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["id_utilisateur"] = request.user
        document = validated_data["id_document"]
        document.statut = validated_data["decision"]
        document.save(update_fields=["statut"])
        return super().create(validated_data)
