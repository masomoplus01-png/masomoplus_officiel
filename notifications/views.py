from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.select_related("id_utilisateur")
    serializer_class = NotificationSerializer
    # MODE TEST - temporary: old security was IsAuthenticated
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def get_queryset(self):
        if getattr(self.request.user, "is_anonymous", False):
            return super().get_queryset()
        return super().get_queryset().filter(id_utilisateur=self.request.user)

    def perform_create(self, serializer):
        serializer.save(id_utilisateur=self.request.user)

    @action(detail=True, methods=["patch"], url_path="read")
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.lu = True
        notification.save(update_fields=["lu"])
        return Response(self.get_serializer(notification).data)
