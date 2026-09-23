from rest_framework import serializers

from .models import Actualite


class ActualiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actualite
        fields = [
            "id_actualite",
            "code_actualite",
            "titre",
            "contenu",
            "image",
            "date_publication",
            "id_auteur",
        ]
        read_only_fields = ["id_actualite", "date_publication", "id_auteur"]
