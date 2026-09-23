from rest_framework import serializers

from .models import Categorie, Faculté, Département, Filière


class FacultéSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculté
        fields = "__all__"


class DépartementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Département
        fields = "__all__"


class FilièreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filière
        fields = "__all__"


class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = "__all__"