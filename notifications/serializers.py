from rest_framework import serializers

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "id_notification",
            "code_notification",
            "titre",
            "contenu",
            "type",
            "lu",
            "date_notification",
            "id_utilisateur",
        ]
        read_only_fields = ["id_notification", "date_notification", "id_utilisateur"]
