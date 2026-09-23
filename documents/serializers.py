from rest_framework import serializers

from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    fichier = serializers.FileField(required=True)
    couverture = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Document
        fields = (
            "id_document",
            "code_document",
            "titre",
            "resume",
            "mots_cles",
            "fichier",
            "couverture",
            "annee_publication",
            "langue",
            "nombre_pages",
            "statut",
            "date_depot",
            "id_categorie",
            "id_filiere",
            "id_utilisateur",
        )
        read_only_fields = ("id_document", "date_depot", "id_utilisateur")

    def validate_fichier(self, value):
        name = value.name.lower() if hasattr(value, "name") else str(value).lower()
        if not name.endswith(".pdf"):
            raise serializers.ValidationError("Le fichier doit être au format PDF.")
        return value

    def validate_couverture(self, value):
        if value is None:
            return value
        name = value.name.lower() if hasattr(value, "name") else str(value).lower()
        valid_ext = (".jpg", ".jpeg", ".png", ".webp")
        if not name.endswith(valid_ext):
            raise serializers.ValidationError("La couverture doit être une image JPG, JPEG, PNG ou WEBP.")
        return value

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["id_utilisateur"] = request.user
        return super().create(validated_data)
